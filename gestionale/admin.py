from django.contrib import admin

from .models import Auto, Azienda, Cliente, DettaglioVendita, Dipendente, Manutenzione, Marca, Privato, Vendita

admin.site.register(Marca)
admin.site.register(Auto)
admin.site.register(Cliente)
admin.site.register(Privato)
admin.site.register(Azienda)
admin.site.register(Dipendente)
admin.site.register(Vendita)
admin.site.register(DettaglioVendita)
admin.site.register(Manutenzione)
