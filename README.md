# Sistema Informativo per Concessionaria Auto

Progetto d'esame di Antonio Esposito — Ingegneria e Scienze Informatiche per la Cybersecurity, Università degli Studi di Napoli Parthenope.

Sistema informativo Django per la gestione di una concessionaria automobilistica: catalogo veicoli, anagrafica clienti (privati e aziende), vendite e manutenzioni.

La documentazione completa del progetto — modello E-R, modello logico, scelte progettuali, istruzioni di installazione e avvio — si trova in [`documentazione/Documentazione.md`](documentazione/Documentazione.md).

## Avvio rapido

```bash
git clone <URL-repository>
cd <nome-cartella-progetto>
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata dati_esempio.json
python manage.py runserver
```
