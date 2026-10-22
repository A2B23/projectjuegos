from django.contrib import admin
from .models import Genero, Juego


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]


@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ["titulo", "tipo", "creador", "fecha_agregado"]
    list_filter = ["tipo", "generos"]
    search_fields = ["titulo", "creador"]
