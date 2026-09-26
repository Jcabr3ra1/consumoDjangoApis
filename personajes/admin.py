from django.contrib import admin

from .models import Aventura, Hermandad, Personaje


@admin.register(Hermandad)
class HermandadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "reino", "faccion")
    list_filter = ("faccion",)
    search_fields = ("nombre", "reino")


@admin.register(Personaje)
class PersonajeAdmin(admin.ModelAdmin):
    list_display = ("nombre", "reino", "faccion", "clase", "nivel", "hermandad")
    list_filter = ("faccion", "clase", "reino")
    search_fields = ("nombre", "reino", "raza")


@admin.register(Aventura)
class AventuraAdmin(admin.ModelAdmin):
    list_display = ("titulo", "personaje", "zona", "tipo", "fecha")
    list_filter = ("tipo", "fecha")
    search_fields = ("titulo", "zona", "personaje__nombre")
