from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, DateField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


# Form per aggiungere una garanzia
class GaranziaForm(FlaskForm):
    nome_oggetto = StringField('Nome Oggetto', validators=[DataRequired()])
    data_acquisto = DateField('Data Acquisto', format='%Y-%m-%d', validators=[DataRequired()])
    fine_garanzia = DateField('Fine Garanzia', format='%Y-%m-%d', validators=[DataRequired()])
    luogo_acquisto = StringField('Luogo di Acquisto')
    note = StringField('Note')

# Form di registrazione User
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

# Form del Profilo
class ProfiloForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=3, max=35)])
    cognome = StringField('Cognome', validators=[DataRequired(), Length(min=3, max=50)])
    data_nascita = DateField('Data di Nascita', validators=[Optional()], format='%Y-%m-%d')
    biografia = TextAreaField('Biografia', validators=[Optional(), Length(max=500)])
    foto_profilo = FileField('Foto Profilo', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Solo immagini!')])