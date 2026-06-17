"""
Comando di gestione per popolare il database con dati di esempio realistici.
Eseguire con: python manage.py popola_db
Il comando è idempotente: se i dati esistono già non li duplica.
"""

from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from gestionale.models import (Auto, Azienda, Cliente, DettaglioVendita,
                                Dipendente, Fornitore, Manutenzione, Marca,
                                Privato, Vendita)


class Command(BaseCommand):
    help = 'Popola il database con dati di esempio per la concessionaria.'

    def handle(self, *args, **options):
        self.stdout.write('Popolamento database in corso...')

        # --- Marche ---
        marche_dati = [
            ('Fiat', 'Italia'), ('BMW', 'Germania'), ('Toyota', 'Giappone'),
            ('Ford', 'USA'), ('Volkswagen', 'Germania'), ('Renault', 'Francia'),
        ]
        marche = {}
        for nome, paese in marche_dati:
            m, _ = Marca.objects.get_or_create(nome=nome, defaults={'paese': paese})
            marche[nome] = m

        # --- Fornitori ---
        fornitori_dati = [
            ('AutoImport Italia Srl', 'Italia'),
            ('EuroMotors GmbH', 'Germania'),
            ('Pacific Auto Trading', 'Giappone'),
        ]
        fornitori = {}
        for nome, paese in fornitori_dati:
            f, _ = Fornitore.objects.get_or_create(nome=nome, defaults={'paese': paese})
            fornitori[nome] = f

        fi = fornitori['AutoImport Italia Srl']
        fe = fornitori['EuroMotors GmbH']
        fp = fornitori['Pacific Auto Trading']

        # --- Auto ---
        auto_dati = [
            ('Panda', 12500, 2021, 'venduta', 'Fiat', fi),
            ('500', 15900, 2022, 'disponibile', 'Fiat', fi),
            ('Tipo', 18700, 2020, 'disponibile', 'Fiat', fi),
            ('Serie 3', 42000, 2023, 'disponibile', 'BMW', fe),
            ('Serie 5', 58000, 2022, 'disponibile', 'BMW', fe),
            ('X3', 63000, 2023, 'disponibile', 'BMW', fe),
            ('Corolla', 24500, 2022, 'disponibile', 'Toyota', fp),
            ('Yaris', 19800, 2021, 'disponibile', 'Toyota', fp),
            ('RAV4', 35000, 2023, 'disponibile', 'Toyota', fp),
            ('Focus', 22000, 2020, 'venduta', 'Ford', fi),
            ('Golf', 28000, 2021, 'venduta', 'Volkswagen', fe),
            ('Clio', 17500, 2022, 'manutenzione', 'Renault', fe),
        ]
        auto_obj = []
        for modello, prezzo, anno, stato, marca_nome, fornitore in auto_dati:
            a, _ = Auto.objects.get_or_create(
                modello=modello,
                marca=marche[marca_nome],
                defaults={
                    'prezzo': prezzo,
                    'anno': anno,
                    'stato': stato,
                    'fornitore': fornitore,
                },
            )
            auto_obj.append(a)

        focus = Auto.objects.get(modello='Focus', marca=marche['Ford'])
        golf = Auto.objects.get(modello='Golf', marca=marche['Volkswagen'])
        clio = Auto.objects.get(modello='Clio', marca=marche['Renault'])

        # --- Dipendenti ---
        dip_dati = [
            ('Marco', 'Bianchi', 'Venditore', 2200),
            ('Laura', 'Rossi', 'Responsabile vendite', 3100),
            ('Giorgio', 'Ferri', 'Venditore', 2000),
        ]
        dipendenti = []
        for nome, cognome, ruolo, stipendio in dip_dati:
            d, _ = Dipendente.objects.get_or_create(
                nome=nome, cognome=cognome,
                defaults={'ruolo': ruolo, 'stipendio': stipendio},
            )
            dipendenti.append(d)

        # --- Clienti privati ---
        privati_dati = [
            ('mario_rossi', 'mario.rossi@email.it', 'Mario', 'Rossi',
             'RSSMRA85M01H501Z', date(1985, 8, 1), '3331112233', 'Roma'),
            ('anna_verdi', 'anna.verdi@email.it', 'Anna', 'Verdi',
             'VRDNNA90A41L219V', date(1990, 1, 41 - 40), '3342223344', 'Milano'),
            ('luca_neri', 'luca.neri@email.it', 'Luca', 'Neri',
             'NRELCU78C15F205X', date(1978, 3, 15), '3353334455', 'Napoli'),
        ]
        clienti_privati = []
        for username, email, nome, cognome, cf, nascita, tel, citta in privati_dati:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password='Password123!')
                cliente = Cliente.objects.create(
                    user=user, tipo_cliente=Cliente.PRIVATO,
                    email=email, telefono=tel, citta=citta,
                )
                Privato.objects.create(
                    cliente=cliente, codice_fiscale=cf,
                    nome=nome, cognome=cognome, data_nascita=nascita,
                )
                clienti_privati.append(cliente)
            else:
                clienti_privati.append(User.objects.get(username=username).cliente)

        # --- Clienti aziendali ---
        aziende_dati = [
            ('flotta_srl', 'info@flottasrl.it', 'Flotta Srl', '12345678901',
             'Trasporti', '0612345678', 'Roma'),
            ('tecno_auto', 'acquisti@tecnoauto.it', 'TecnoAuto SpA', '98765432101',
             'Tecnologia', '0298765432', 'Milano'),
        ]
        clienti_aziende = []
        for username, email, rs, piva, settore, tel, citta in aziende_dati:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password='Password123!')
                cliente = Cliente.objects.create(
                    user=user, tipo_cliente=Cliente.AZIENDA,
                    email=email, telefono=tel, citta=citta,
                )
                Azienda.objects.create(
                    cliente=cliente, partita_iva=piva,
                    ragione_sociale=rs, settore=settore,
                )
                clienti_aziende.append(cliente)
            else:
                clienti_aziende.append(User.objects.get(username=username).cliente)

        # --- Vendite ---
        if not Vendita.objects.filter(pk=1).exists():
            v1 = Vendita.objects.create(
                data_vendita=date(2024, 3, 10),
                importo_totale=22000,
                cliente=clienti_privati[0],
                dipendente=dipendenti[0],
            )
            DettaglioVendita.objects.create(
                vendita=v1, auto=focus, quantita=1, prezzo_unitario=22000,
            )

            v2 = Vendita.objects.create(
                data_vendita=date(2024, 6, 5),
                importo_totale=28000,
                cliente=clienti_aziende[0],
                dipendente=dipendenti[1],
            )
            DettaglioVendita.objects.create(
                vendita=v2, auto=golf, quantita=1, prezzo_unitario=28000,
            )

            v3 = Vendita.objects.create(
                data_vendita=date(2024, 9, 20),
                importo_totale=12500,
                cliente=clienti_privati[1],
                dipendente=dipendenti[2],
            )
            DettaglioVendita.objects.create(
                vendita=v3,
                auto=Auto.objects.get(modello='Panda', marca=marche['Fiat']),
                quantita=1, prezzo_unitario=12500,
            )

        # --- Manutenzioni ---
        manutenzioni_dati = [
            (clio, date(2024, 1, 15), 'Tagliando ordinario', 320),
            (clio, date(2024, 5, 3), 'Sostituzione pastiglie freno', 180),
            (clio, date(2024, 11, 22), 'Revisione climatizzatore', 95),
            (focus, date(2023, 8, 10), 'Tagliando + cambio olio', 280),
            (golf, date(2023, 12, 1), 'Sostituzione cinghia distribuzione', 550),
            (Auto.objects.get(modello='Serie 3', marca=marche['BMW']),
             date(2024, 7, 19), 'Controllo freni e pneumatici', 210),
        ]
        for auto, data, desc, costo in manutenzioni_dati:
            Manutenzione.objects.get_or_create(
                auto=auto, data_intervento=data,
                defaults={'descrizione': desc, 'costo': costo},
            )

        self.stdout.write(self.style.SUCCESS(
            'Database popolato con successo!\n'
            'Credenziali clienti di esempio (password: Password123!):\n'
            '  privati : mario_rossi, anna_verdi, luca_neri\n'
            '  aziende : flotta_srl, tecno_auto'
        ))
