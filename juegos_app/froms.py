from django import forms
from .models import Juego


class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = [
            "titulo",
            "descripcion",
            "imagen",
            "tipo",
            "url",
            "generos",
            "creador",
            "fecha_agregado",
        ]
        widgets = {
            "fecha_agregado": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
        }