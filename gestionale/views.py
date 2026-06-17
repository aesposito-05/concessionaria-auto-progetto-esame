from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RicercaAutoForm, RegistrazioneAziendaForm, RegistrazionePrivatoForm
from .models import Auto, Manutenzione, Vendita


def home(request):
    totale_auto = Auto.objects.filter(stato=Auto.DISPONIBILE).count()
    return render(request, 'gestionale/home.html', {'totale_auto': totale_auto})


def registrazione_scelta(request):
    return render(request, 'gestionale/registrazione_scelta.html')


def registrazione_privato(request):
    if request.method == 'POST':
        form = RegistrazionePrivatoForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrazionePrivatoForm()
    return render(request, 'gestionale/registrazione_privato.html', {'form': form})


def registrazione_azienda(request):
    if request.method == 'POST':
        form = RegistrazioneAziendaForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrazioneAziendaForm()
    return render(request, 'gestionale/registrazione_azienda.html', {'form': form})


def ricerca_auto(request):
    form = RicercaAutoForm(request.GET or None)
    qs = Auto.objects.select_related('marca').filter(stato=Auto.DISPONIBILE).order_by('marca__nome', 'modello')
    if form.is_valid():
        if form.cleaned_data.get('marca'):
            qs = qs.filter(marca__nome__icontains=form.cleaned_data['marca'])
        if form.cleaned_data.get('modello'):
            qs = qs.filter(modello__icontains=form.cleaned_data['modello'])
        if form.cleaned_data.get('prezzo_min') is not None:
            qs = qs.filter(prezzo__gte=form.cleaned_data['prezzo_min'])
        if form.cleaned_data.get('prezzo_max') is not None:
            qs = qs.filter(prezzo__lte=form.cleaned_data['prezzo_max'])
    return render(request, 'gestionale/ricerca_auto.html', {'form': form, 'auto_list': qs})


def dettaglio_auto(request, pk):
    auto = get_object_or_404(
        Auto.objects.select_related('marca', 'fornitore'), pk=pk
    )
    return render(request, 'gestionale/dettaglio_auto.html', {'auto': auto})


@login_required
def storico_vendite(request):
    try:
        cliente = request.user.cliente
    except Exception:
        return render(request, 'gestionale/storico_vendite.html', {
            'vendite': [],
            'no_cliente': True,
        })
    vendite = (
        Vendita.objects.filter(cliente=cliente)
        .prefetch_related('dettagli__auto__marca')
        .select_related('dipendente')
    )
    return render(request, 'gestionale/storico_vendite.html', {'vendite': vendite})


def storico_manutenzioni(request):
    auto_list = Auto.objects.select_related('marca').order_by('marca__nome', 'modello')
    auto_selezionata = None
    manutenzioni = None
    auto_id = request.GET.get('auto')
    if auto_id:
        auto_selezionata = get_object_or_404(Auto, pk=auto_id)
        manutenzioni = Manutenzione.objects.filter(auto=auto_selezionata)
    return render(request, 'gestionale/storico_manutenzioni.html', {
        'auto_list': auto_list,
        'auto_selezionata': auto_selezionata,
        'manutenzioni': manutenzioni,
    })
