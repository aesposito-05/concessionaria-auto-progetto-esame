from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registrazione/', views.registrazione_scelta, name='registrazione_scelta'),
    path('registrazione/privato/', views.registrazione_privato, name='registrazione_privato'),
    path('registrazione/azienda/', views.registrazione_azienda, name='registrazione_azienda'),
    path('auto/', views.ricerca_auto, name='ricerca_auto'),
    path('auto/<int:pk>/', views.dettaglio_auto, name='dettaglio_auto'),
    path('le-mie-vendite/', views.storico_vendite, name='storico_vendite'),
    path('manutenzioni/', views.storico_manutenzioni, name='storico_manutenzioni'),
]
