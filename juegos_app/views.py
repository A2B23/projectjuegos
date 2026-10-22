from django.shortcuts import render, get_object_or_404
from .models import Juego, Genero


def lista_juegos(request):
    tipo = request.GET.get("tipo")
    juegos = Juego.objects.prefetch_related("generos")
    if tipo in ("instalable", "web"):
        juegos = juegos.filter(tipo=tipo)
    return render(request, "juegos_app/lista.html", {"juegos": juegos, "tipo": tipo})


def detalle_juego(request, pk):
    juego = get_object_or_404(Juego, pk=pk)
    return render(request, "juegos_app/detalle.html", {"juego": juego})