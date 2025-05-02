from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, EmailField
from wtforms.validators import DataRequired, Email, Length

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