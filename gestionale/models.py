"""
Modelli Django che traducono lo schema logico relazionale descritto nella
documentazione di progetto (sezione 2). Ogni tabella SQL ha qui una
corrispondenza 1:1 con un modello, comprese le chiavi esterne e i vincoli
espressi tramite validators/choices.
"""

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Marca(models.Model):
    nome = models.CharField(max_length=50)
    paese = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = 'marche'

    def __str__(self):
        return self.nome


class Fornitore(models.Model):
    nome = models.CharField(max_length=50)
    paese = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nome


class Auto(models.Model):
    DISPONIBILE = 'disponibile'
    VENDUTA = 'venduta'
    IN_MANUTENZIONE = 'manutenzione'
    STATO_CHOICES = [
        (DISPONIBILE, 'Disponibile'),
        (VENDUTA, 'Venduta'),
        (IN_MANUTENZIONE, 'In manutenzione'),
    ]

    modello = models.CharField(max_length=50)
    prezzo = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    anno = models.PositiveIntegerField(null=True, blank=True)
    stato = models.CharField(max_length=20, choices=STATO_CHOICES, default=DISPONIBILE)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='auto')
    fornitore = models.ForeignKey(Fornitore, on_delete=models.PROTECT, related_name='auto')

    class Meta:
        verbose_name_plural = 'auto'

    def __str__(self):
        return f'{self.marca} {self.modello}'


class Cliente(models.Model):
    """Entita' generalizzata. Gli attributi specifici di Privato e Azienda
    vivono nelle rispettive tabelle figlie (vedi sotto), in relazione 1:1
    con questa tabella tramite chiave primaria condivisa."""

    PRIVATO = 'privato'
    AZIENDA = 'azienda'
    TIPO_CHOICES = [
        (PRIVATO, 'Privato'),
        (AZIENDA, 'Azienda'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    tipo_cliente = models.CharField(max_length=10, choices=TIPO_CHOICES)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    citta = models.CharField(max_length=50, blank=True)

    def __str__(self):
        # Mostra il nome/ragione sociale della specializzazione corretta.
        if self.tipo_cliente == self.PRIVATO and hasattr(self, 'privato'):
            return f'{self.privato.nome} {self.privato.cognome}'
        if self.tipo_cliente == self.AZIENDA and hasattr(self, 'azienda'):
            return self.azienda.ragione_sociale
        return self.email

    @property
    def nome_visualizzato(self):
        return str(self)


class Privato(models.Model):
    """Specializzazione di Cliente per le persone fisiche."""

    cliente = models.OneToOneField(
        Cliente, on_delete=models.CASCADE, related_name='privato'
    )
    codice_fiscale = models.CharField(max_length=16, unique=True)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    data_nascita = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.nome} {self.cognome}'


class Azienda(models.Model):
    """Specializzazione di Cliente per le persone giuridiche."""

    cliente = models.OneToOneField(
        Cliente, on_delete=models.CASCADE, related_name='azienda'
    )
    partita_iva = models.CharField(max_length=11, unique=True)
    ragione_sociale = models.CharField(max_length=100)
    settore = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.ragione_sociale


class Dipendente(models.Model):
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    ruolo = models.CharField(max_length=50, blank=True)
    stipendio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.nome} {self.cognome}'


class Vendita(models.Model):
    data_vendita = models.DateField()
    importo_totale = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='vendite')
    dipendente = models.ForeignKey(Dipendente, on_delete=models.PROTECT, related_name='vendite')

    class Meta:
        verbose_name_plural = 'vendite'
        ordering = ['-data_vendita']

    def __str__(self):
        return f'Vendita #{self.pk} - {self.cliente}'


class DettaglioVendita(models.Model):
    """Tabella ponte che risolve la relazione N:M tra Vendita e Auto."""

    vendita = models.ForeignKey(Vendita, on_delete=models.CASCADE, related_name='dettagli')
    auto = models.ForeignKey(Auto, on_delete=models.PROTECT, related_name='dettagli_vendita')
    quantita = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    prezzo_unitario = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )

    class Meta:
        verbose_name_plural = 'dettagli vendita'
        constraints = [
            models.UniqueConstraint(fields=['vendita', 'auto'], name='unique_vendita_auto')
        ]

    def __str__(self):
        return f'{self.auto} x{self.quantita} (vendita #{self.vendita_id})'

    @property
    def subtotale(self):
        return self.quantita * self.prezzo_unitario


class Manutenzione(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name='manutenzioni')
    data_intervento = models.DateField(null=True, blank=True)
    descrizione = models.CharField(max_length=100, blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['-data_intervento']

    def __str__(self):
        return f'{self.auto} - {self.descrizione or "intervento"}'
