@echo off
echo Avvio server Concessionaria Auto...
cd /d "C:\Users\Utente\Desktop\progetto_concessionaria_parziale"
call venv\Scripts\activate
start "" "http://127.0.0.1:8000/"
start "" "http://127.0.0.1:8000/admin/"
python manage.py runserver
