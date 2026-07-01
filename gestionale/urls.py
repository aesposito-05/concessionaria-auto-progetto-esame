from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auto/', views.lista_auto, name='lista_auto'),
    path('auto/<int:pk>/', views.dettaglio_auto, name='dettaglio_auto'),
]
