
# 🛡️ Garanzie Manager - Applicazione Web Flask

## Descrizione del Progetto

**Gestione Garanzie** è un'applicazione web sviluppata con Flask e MongoDB che consente agli utenti registrati di gestire in modo semplice ed efficace le garanzie dei propri prodotti acquistati.  
Gli utenti possono registrarsi, accedere, caricare foto e scontrini, e monitorare le date di scadenza delle garanzie in una dashboard personale.

### Funzionalità Principali

- Registrazione e login utenti
- Autenticazione sicura con Flask-Login
- Dashboard utente con elenco garanzie
- Aggiunta garanzie con upload di immagini (oggetto e scontrino)
- Salvataggio persistente in MongoDB
- UI tramite template HTML (Jinja2)

---

## 🧰 Stack Tecnologico

- **Flask**: Framework web backend
- **MongoEngine**: ODM per MongoDB
- **Flask-Login**: Gestione sessioni utente
- **WTForms**: Gestione e validazione dei form
- **MongoDB**: Database NoSQL
- **HTML/CSS**: Frontend con template Jinja2

---


## 🧪 Prerequisiti

- Python 3.8 o superiore
- MongoDB installato e in esecuzione su `localhost:27017`
- Ambiente virtuale (consigliato)

---

## ⚙️ Setup del Progetto

### 1. Clonare il repository

```bash
git clone https://github.com/JavaSoftwareEntwickler/garanzie-manager.git
cd garanzie-manager
````

### 2. Creare ed attivare un ambiente virtuale

```bash
python -m venv venv
source venv/bin/activate   # Su Windows: venv\Scripts\activate
```

### 3. Installare le dipendenze

```bash
pip install -r requirements.txt
```

### 4. Avviare MongoDB

Assicurati che MongoDB sia installato.Avvialo e 
crea il db garanzie_db e 
crea due collection:
garanzia e user

### 5. Avviare l'app Flask

```bash
python -m flask run
```

> L'applicazione sarà disponibile all'indirizzo: [http://localhost:5000](http://localhost:5000)

---

## 🔐 Credenziali di Default (opzionale)

Nel caso si voglia popolare il DB con un utente di test:

```bash
{
  "username": "test",
  "password": "testtest",
  "email": "test@test.com",
  "profilo": {
    "nome": "test",
    "cognome": "test",
    "biografia": "test"
  }
}
```

*(Può essere inserito via Mongo shell o script Python separato o da MogoDB Compass)*

---

## 📌 Note Aggiuntive

* Le immagini caricate vengono salvate in `static/uploads`.
* I file accettati per upload sono: `.png`, `.jpg`, `.jpeg`, `.gif`.
* Personalizza `SECRET_KEY` in `app.config` per ambienti di produzione.

---

## 🧾 Licenza

Progetto open-source rilasciato sotto licenza MIT.

---

## 🙌 Autore

**Max** - Sviluppatore Backend
Contattami su [LinkedIn](https://www.linkedin.com/in/mmjava/) per collaborazioni, feedback o suggerimenti.
