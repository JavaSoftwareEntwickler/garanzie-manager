from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from models.models import User, Garanzia, Profilo
from forms.forms import RegisterForm, GaranziaForm, ProfiloForm
from mongoengine import connect
from datetime import datetime

import os

# Inizializzazione Flask e MongoDB
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] ='static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
connect(db='garanzie_db', host='localhost', port=27017)

# Gestione login e utenti
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route per la home page
@app.route('/')
def index():
    return render_template('index.html')

# Route per il login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.objects(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Credenziali non valide', 'danger')
    return render_template('login.html')

# Route per registrazione
@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Ottieni i dati dal form
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # Verifica se l'username o la email esistono già nel database
        if User.objects(username=username).first():
            flash('Username già in uso', 'danger')
            return redirect(url_for('register'))

        if User.objects(email=email).first():
            flash('Email già in uso', 'danger')
            return redirect(url_for('register'))

        user = User(username=username, email=email, password=password)
        user.save()
        flash('Registrazione avvenuta con successo!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Dashboard dove gli utenti possono vedere e aggiungere garanzie
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = GaranziaForm()
    if form.validate_on_submit():
        nome_oggetto = form.nome_oggetto.data
        data_acquisto = form.data_acquisto.data
        fine_garanzia = form.fine_garanzia.data
        luogo_acquisto = form.luogo_acquisto.data
        foto_oggetto = None
        scontrino = None
        note = form.note.data

        garanzia = Garanzia(
            user=current_user,
            nome_oggetto=nome_oggetto,
            data_acquisto=data_acquisto,
            fine_garanzia=fine_garanzia,
            luogo_acquisto=luogo_acquisto,
            foto_oggetto=foto_oggetto,
            scontrino=scontrino,
            note=note
        )
        garanzia.save()

        # se non c'è crea la cartella
        # ├── garanzie /
        # │   └── < username > /
        # │       └── < garanzia_id > /

        # Crea la cartella per la garanzia se non esiste
        garanzia_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'garanzie', current_user.username, str(garanzia.id))
        os.makedirs(garanzia_folder, exist_ok=True)

        # 3. Gestione upload foto oggetto
        file_oggetto = request.files.get('foto_oggetto')
        if file_oggetto and file_oggetto.filename:
            ext = os.path.splitext(file_oggetto.filename)[1]
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename_oggetto = f"foto_prodotto_{current_user.username}_{timestamp}{ext}"
            path_oggetto = os.path.join(str(garanzia_folder), filename_oggetto)
            # Salvataggio foto nel path
            file_oggetto.save(path_oggetto)
            # Memorizzazione del path relativo a DB
            path_relativo = os.path.join('uploads','garanzie', current_user.username, str(garanzia.id), filename_oggetto)
            garanzia.foto_oggetto = path_relativo.replace(os.path.sep, '/')

        # 4. Gestione upload scontrino
        file_scontrino = request.files.get('scontrino')
        if file_scontrino and file_scontrino.filename:
            ext = os.path.splitext(file_scontrino.filename)[1]
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename_scontrino = f"foto_scontrino_{current_user.username}_{timestamp}{ext}"
            path_scontrino = os.path.join(str(garanzia_folder), filename_scontrino)
            # Salvataggio foto nel path
            file_scontrino.save(path_scontrino)
            # Memorizzazione del path relativo a DB

            path_relativo = os.path.join('uploads','garanzie', current_user.username, str(garanzia.id), filename_scontrino)
            garanzia.scontrino = path_relativo.replace(os.path.sep, '/')

        # Aggiorna garanzia con i path delle immagini
        garanzia.save()

        flash('Garanzia aggiunta con successo!', 'success')
        return redirect(url_for('dashboard'))

    garanzie = Garanzia.objects(user=current_user)
    return render_template('dashboard.html', form=form, garanzie=garanzie)


@app.route('/profilo', methods=['GET', 'POST'])
def profilo():
    if request.method == 'POST':
        pass
    return render_template('profilo.html')

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user._get_current_object()
    form = ProfiloForm(obj=user.profilo)  # precompila se esiste

    if form.validate_on_submit():
        if not user.profilo:
            user.profilo = Profilo()

        user.profilo.nome = form.nome.data
        user.profilo.cognome = form.cognome.data
        user.profilo.data_nascita = form.data_nascita.data
        user.profilo.luogo_nascita = form.luogo_nascita.data
        user.profilo.biografia = form.biografia.data

        # se non c'è crea la cartella
        # uploads /
        # ├── profili /
        # │   └── < username > /

        # Crea la cartella per la garanzia se non esiste
        profilo_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'profili', current_user.username)
        os.makedirs(profilo_folder, exist_ok=True)
        print(profilo_folder)

        # Gestione upload foto profilo
        file_profilo = request.files.get('foto')

        if file_profilo and file_profilo.filename:

            # Se esiste una foto precedente, la cancelliamo
            if user.profilo.foto:
                # Ottieni il percorso del file precedente
                foto_precedente = os.path.join('static', user.profilo.foto)
                # Controlla se il file esiste e cancellalo
                if os.path.exists(foto_precedente):
                    os.remove(foto_precedente)

            ext = os.path.splitext(file_profilo.filename)[1]
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename_profilo = f"foto_profilo_{current_user.username}_{timestamp}{ext}"

            # Salvataggio foto
            path_oggetto = os.path.join(str(profilo_folder), filename_profilo)
            file_profilo.save(path_oggetto)
            # Memorizzazione del path relativo nel DB (senza "static/")
            path_relativo = os.path.join('uploads', 'profili', current_user.username, filename_profilo)
            user.profilo.foto = path_relativo.replace(os.path.sep, '/')

        user.save()
        flash('Profilo aggiornato con successo', 'success')
        return redirect(url_for('profilo'))

    return render_template('edit-profile.html', form=form)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
