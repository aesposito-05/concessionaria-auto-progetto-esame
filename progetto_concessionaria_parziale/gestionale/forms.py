from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Azienda, Cliente, Privato


class RegistrazionePrivatoForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    telefono = forms.CharField(max_length=20, required=False, label='Telefono')
    citta = forms.CharField(max_length=50, required=False, label='Città')
    nome = forms.CharField(max_length=50, label='Nome')
    cognome = forms.CharField(max_length=50, label='Cognome')
    codice_fiscale = forms.CharField(max_length=16, label='Codice fiscale')
    data_nascita = forms.DateField(
        required=False,
        label='Data di nascita',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_codice_fiscale(self):
        cf = self.cleaned_data['codice_fiscale'].upper()
        if Privato.objects.filter(codice_fiscale=cf).exists():
            raise forms.ValidationError('Codice fiscale già registrato.')
        return cf

    def clean_email(self):
        email = self.cleaned_data['email']
        if Cliente.objects.filter(email=email).exists():
            raise forms.ValidationError('Email già registrata.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            cliente = Cliente.objects.create(
                user=user,
                tipo_cliente=Cliente.PRIVATO,
                email=self.cleaned_data['email'],
                telefono=self.cleaned_data.get('telefono', ''),
                citta=self.cleaned_data.get('citta', ''),
            )
            Privato.objects.create(
                cliente=cliente,
                codice_fiscale=self.cleaned_data['codice_fiscale'],
                nome=self.cleaned_data['nome'],
                cognome=self.cleaned_data['cognome'],
                data_nascita=self.cleaned_data.get('data_nascita'),
            )
        return user


class RegistrazioneAziendaForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    telefono = forms.CharField(max_length=20, required=False, label='Telefono')
    citta = forms.CharField(max_length=50, required=False, label='Città')
    ragione_sociale = forms.CharField(max_length=100, label='Ragione sociale')
    partita_iva = forms.CharField(max_length=11, label='Partita IVA')
    settore = forms.CharField(max_length=50, required=False, label='Settore')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_partita_iva(self):
        piva = self.cleaned_data['partita_iva']
        if Azienda.objects.filter(partita_iva=piva).exists():
            raise forms.ValidationError('Partita IVA già registrata.')
        return piva

    def clean_email(self):
        email = self.cleaned_data['email']
        if Cliente.objects.filter(email=email).exists():
            raise forms.ValidationError('Email già registrata.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            cliente = Cliente.objects.create(
                user=user,
                tipo_cliente=Cliente.AZIENDA,
                email=self.cleaned_data['email'],
                telefono=self.cleaned_data.get('telefono', ''),
                citta=self.cleaned_data.get('citta', ''),
            )
            Azienda.objects.create(
                cliente=cliente,
                partita_iva=self.cleaned_data['partita_iva'],
                ragione_sociale=self.cleaned_data['ragione_sociale'],
                settore=self.cleaned_data.get('settore', ''),
            )
        return user


class RicercaAutoForm(forms.Form):
    marca = forms.CharField(max_length=50, required=False, label='Marca')
    modello = forms.CharField(max_length=50, required=False, label='Modello')
    prezzo_min = forms.DecimalField(
        required=False, min_value=0, label='Prezzo minimo (€)',
        widget=forms.NumberInput(attrs={'placeholder': 'es. 10000'}),
    )
    prezzo_max = forms.DecimalField(
        required=False, min_value=0, label='Prezzo massimo (€)',
        widget=forms.NumberInput(attrs={'placeholder': 'es. 50000'}),
    )
