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
        note = form.note.data

        foto_oggetto = None
        scontrino = None

        # Gestione upload foto oggetto e scontrino
        if 'foto_oggetto' in request.files:
            foto_oggetto = secure_filename(request.files['foto_oggetto'].filename)
            name, ext = os.path.splitext(foto_oggetto)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            foto_oggetto = f"{nome_oggetto}_{timestamp}_{name}{ext}"
            request.files['foto_oggetto'].save(os.path.join(app.config['UPLOAD_FOLDER'], foto_oggetto))

        if 'scontrino' in request.files:
            scontrino = secure_filename(request.files['scontrino'].filename)
            name, ext = os.path.splitext(scontrino)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            scontrino = f"{nome_oggetto}_Scontrino_{timestamp}_{name}{ext}"
            request.files['scontrino'].save(os.path.join(app.config['UPLOAD_FOLDER'], scontrino))

        # Salvataggio della garanzia nel DB
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
        user.profilo.biografia = form.biografia.data


        # gestione upload foto
        if form.foto_profilo.data:
            filename = secure_filename(form.foto_profilo.data.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.foto_profilo.data.save(path)
            user.profilo.foto_profilo = filename

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
