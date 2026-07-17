from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionale', '0002_azienda_id_privato_id_alter_azienda_cliente_and_more'),
    ]

    operations = [
        # Trigger 1: aggiorna stato auto a "venduta" dopo inserimento in dettaglio_vendita
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER IF NOT EXISTS aggiorna_stato_auto
                AFTER INSERT ON gestionale_dettagliovendita
                FOR EACH ROW
                BEGIN
                    UPDATE gestionale_auto
                    SET stato = 'venduta'
                    WHERE id = NEW.auto_id;
                END;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS aggiorna_stato_auto;",
        ),

        # Trigger 2: vincolo specializzazione Cliente (privato o azienda)
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER IF NOT EXISTS controlla_specializzazione
                AFTER INSERT ON gestionale_cliente
                FOR EACH ROW
                WHEN NEW.tipo_cliente NOT IN ('privato', 'azienda')
                BEGIN
                    SELECT RAISE(ABORT, 'tipo_cliente deve essere privato o azienda');
                END;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS controlla_specializzazione;",
        ),

        # Trigger 3: ricalcola importo_totale in vendita dopo inserimento in dettaglio_vendita
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER IF NOT EXISTS aggiorna_importo_vendita
                AFTER INSERT ON gestionale_dettagliovendita
                FOR EACH ROW
                BEGIN
                    UPDATE gestionale_vendita
                    SET importo_totale = (
                        SELECT SUM(quantita * prezzo_unitario)
                        FROM gestionale_dettagliovendita
                        WHERE vendita_id = NEW.vendita_id
                    )
                    WHERE id = NEW.vendita_id;
                END;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS aggiorna_importo_vendita;",
        ),
    ]
