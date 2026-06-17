CREATE DATABASE concessionaria_auto;
USE concessionaria_auto;

CREATE TABLE marca (
  id_marca INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(50) NOT NULL,
  paese VARCHAR(50)
);

CREATE TABLE fornitore (
  id_fornitore INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(50) NOT NULL,
  paese VARCHAR(50)
);

CREATE TABLE auto (
  id_auto INT PRIMARY KEY AUTO_INCREMENT,
  modello VARCHAR(50) NOT NULL,
  prezzo DECIMAL(10,2) NOT NULL CHECK (prezzo > 0),
  anno INT,
  stato VARCHAR(20) NOT NULL DEFAULT 'disponibile'
    CHECK (stato IN ('disponibile', 'venduta', 'manutenzione')),
  id_marca INT NOT NULL,
  id_fornitore INT NOT NULL,
  FOREIGN KEY (id_marca) REFERENCES marca(id_marca),
  FOREIGN KEY (id_fornitore) REFERENCES fornitore(id_fornitore)
);

-- Generalizzazione Cliente -> Privato / Azienda (strategia "tabella per ogni entità")
CREATE TABLE cliente (
  id_cliente INT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(100) UNIQUE NOT NULL,
  telefono VARCHAR(20),
  citta VARCHAR(50),
  tipo_cliente VARCHAR(10) NOT NULL CHECK (tipo_cliente IN ('privato', 'azienda'))
);

CREATE TABLE privato (
  id_cliente INT PRIMARY KEY,
  codice_fiscale VARCHAR(16) UNIQUE NOT NULL,
  nome VARCHAR(50) NOT NULL,
  cognome VARCHAR(50) NOT NULL,
  data_nascita DATE,
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE azienda (
  id_cliente INT PRIMARY KEY,
  partita_iva VARCHAR(11) UNIQUE NOT NULL,
  ragione_sociale VARCHAR(100) NOT NULL,
  settore VARCHAR(50),
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE dipendente (
  id_dipendente INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(50) NOT NULL,
  cognome VARCHAR(50) NOT NULL,
  ruolo VARCHAR(50),
  stipendio DECIMAL(10,2)
);

CREATE TABLE vendita (
  id_vendita INT PRIMARY KEY AUTO_INCREMENT,
  data_vendita DATE NOT NULL,
  importo_totale DECIMAL(10,2) DEFAULT 0,
  id_cliente INT NOT NULL,
  id_dipendente INT NOT NULL,
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
  FOREIGN KEY (id_dipendente) REFERENCES dipendente(id_dipendente)
);

-- Tabella ponte per la relazione N:M Vendita <-> Auto
CREATE TABLE dettaglio_vendita (
  id_vendita INT,
  id_auto INT,
  quantita INT NOT NULL CHECK (quantita > 0),
  prezzo_unitario DECIMAL(10,2) NOT NULL CHECK (prezzo_unitario > 0),
  PRIMARY KEY (id_vendita, id_auto),
  FOREIGN KEY (id_vendita) REFERENCES vendita(id_vendita),
  FOREIGN KEY (id_auto) REFERENCES auto(id_auto)
);

CREATE TABLE manutenzione (
  id_manutenzione INT PRIMARY KEY AUTO_INCREMENT,
  data_intervento DATE,
  descrizione VARCHAR(100),
  costo DECIMAL(10,2),
  id_auto INT NOT NULL,
  FOREIGN KEY (id_auto) REFERENCES auto(id_auto)
);
