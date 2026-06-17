"""URL principali del progetto. Includono le rotte dell'app gestionale
e le rotte di autenticazione standard di Django (login/logout)."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('gestionale.urls')),
]
