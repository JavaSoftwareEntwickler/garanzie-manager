from flask_login import UserMixin
from mongoengine import (
    Document, StringField, DateField, ReferenceField,
    DateField, EmbeddedDocument, EmbeddedDocumentField
)

class Profilo(EmbeddedDocument):
    nome = StringField(max_length=35)
    cognome = StringField(max_length=50)
    data_nascita = DateField()
    biografia = StringField(max_length=500)
    foto_profilo = StringField()  # path dell'immagine

class User(Document, UserMixin):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = StringField(required=True, unique=True)
    profilo = EmbeddedDocumentField(Profilo)  # campo opzionale

class Garanzia(Document):
    user = ReferenceField(User, required=True)
    nome_oggetto = StringField(required=True)
    data_acquisto = DateField(required=True)
    fine_garanzia = DateField(required=True)
    luogo_acquisto = StringField()
    foto_oggetto = StringField()
    scontrino = StringField()
    note = StringField()
