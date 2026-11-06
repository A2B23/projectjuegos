from rest_framework import serializers
from .models import Juego


class JuegoSerializer(serializers.ModelSerializer):
    generos = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Juego
        fields = ["id", "titulo", "descripcion", "imagen", "tipo", "url", "generos"]