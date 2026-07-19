-- ============================================================
-- Trigger della concessionaria auto
-- Implementano i vincoli interrelazionali della sezione 1.8
-- ============================================================

-- Trigger 1: aggiorna lo stato dell'auto a "venduta" dopo una vendita
CREATE TRIGGER aggiorna_stato_auto
AFTER INSERT ON dettaglio_vendita
FOR EACH ROW
BEGIN
    UPDATE auto
    SET stato = 'venduta'
    WHERE id_auto = NEW.id_auto;
END;

-- Trigger 2: vincolo interrelazionale sulla specializzazione Cliente
CREATE TRIGGER controlla_specializzazione
AFTER INSERT ON cliente
FOR EACH ROW
BEGIN
    IF NEW.tipo_cliente NOT IN ('privato', 'azienda') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'tipo_cliente deve essere privato o azienda';
    END IF;
END;

-- Trigger 3: aggiorna l'importo totale della vendita dopo ogni dettaglio
CREATE TRIGGER aggiorna_importo_vendita
AFTER INSERT ON dettaglio_vendita
FOR EACH ROW
BEGIN
    UPDATE vendita
    SET importo_totale = (
        SELECT SUM(quantita * prezzo_unitario)
        FROM dettaglio_vendita
        WHERE id_vendita = NEW.id_vendita
    )
    WHERE id_vendita = NEW.id_vendita;
END;
