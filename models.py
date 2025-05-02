from flask_login import UserMixin
from mongoengine import Document, StringField, DateField, ReferenceField

class User(Document, UserMixin):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = StringField(required=True, unique=True)

class Garanzia(Document):
    user = ReferenceField(User, required=True)
    nome_oggetto = StringField(required=True)
    data_acquisto = DateField(required=True)
    fine_garanzia = DateField(required=True)
    luogo_acquisto = StringField()
    foto_oggetto = StringField()
    scontrino = StringField()
    note = StringField()
