from django.shortcuts import get_object_or_404, render

from .models import Auto


def home(request):
    totale_auto = Auto.objects.filter(stato=Auto.DISPONIBILE).count()
    return render(request, 'gestionale/home.html', {'totale_auto': totale_auto})


def lista_auto(request):
    auto_list = Auto.objects.select_related('marca').filter(stato=Auto.DISPONIBILE)
    return render(request, 'gestionale/ricerca_auto.html', {'auto_list': auto_list})


def dettaglio_auto(request, pk):
    auto = get_object_or_404(Auto.objects.select_related('marca', 'fornitore'), pk=pk)
    return render(request, 'gestionale/dettaglio_auto.html', {'auto': auto})
