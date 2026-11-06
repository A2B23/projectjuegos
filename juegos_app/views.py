import json
import random
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlencode
from urllib.request import Request, urlopen

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET
from .models import Juego, Genero
from .froms import JuegoForm
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import JuegoSerializer
from rest_framework.pagination import PageNumberPagination

def crear_juego(request):
    form = JuegoForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Juego creado correctamente.")
        return redirect("juegos_app:lista")  

    return render(request, "crear_juego.html", {"form": form})


def lista_juegos(request):
    tipo = request.GET.get("tipo")
    titulo = request.GET.get("titulo", "").strip()

    juegos = Juego.objects.prefetch_related("generos")

    if tipo in ("instalable", "web"):
        juegos = juegos.filter(tipo=tipo)

    if titulo:
        juegos = juegos.filter(titulo__icontains=titulo)

    return render(
        request,
        "juegos_app/lista.html",
        {"juegos": juegos, "tipo": tipo, "titulo": titulo},
    )


def detalle_juego(request, pk):
    juego = get_object_or_404(Juego, pk=pk)
    return render(request, "juegos_app/detalle.html", {"juego": juego})



def editar_juego(request, pk):
    juego = get_object_or_404(Juego, pk=pk)

    if request.method == "POST":
        form = JuegoForm(request.POST, request.FILES, instance=juego)
        if form.is_valid():
            form.save()
            messages.success(request, "Juego modificado correctamente.")
            return redirect("juegos_app:editar", pk=juego.pk)
    else:
        form = JuegoForm(instance=juego)

    form.fields["descripcion"].disabled = True

    return render(
        request,
        "juegos_app/editar.html",
        {
            "juego": juego,
            "form": form,
            "titulo": f"Editar {juego.titulo}",
        },
    )


def eliminar_juego(request, pk):
    juego = get_object_or_404(Juego, pk=pk)

    if request.method == "POST":
        juego.delete()
        messages.success(request, "Juego eliminado correctamente.")
        return redirect("juegos_app:lista")

    return render(
        request,
        "juegos_app/eliminar.html",
        {"juego": juego},
    )


@api_view(["GET"])
def api_juegos(request):
    juegos = Juego.objects.all()

    tipo = request.query_params.get("tipo")
    titulo = request.query_params.get("titulo")
    genero = request.query_params.get("genero")

    if tipo in ("web", "instalable"):
        juegos = juegos.filter(tipo=tipo)

    if titulo:
        juegos = juegos.filter(titulo__icontains=titulo)

    if genero:
        juegos = juegos.filter(
            generos__nombre__icontains=genero
        ).distinct()

    paginador = PageNumberPagination()
    paginador.page_size = 5

    pagina = paginador.paginate_queryset(juegos, request)
    serializer = JuegoSerializer(pagina, many=True)

    return paginador.get_paginated_response(serializer.data)


def trivia_videojuegos(request):
    return render(request, "juegos_app/trivia.html")


@require_GET
def api_trivia_pregunta(request):
    dificultad = request.GET.get("dificultad", "medium")
    if dificultad not in ("easy", "medium", "hard"):
        dificultad = "medium"

    clave_cache = f"opentdb:videojuegos:{dificultad}"
    preguntas = cache.get(clave_cache)

    if not preguntas:
        parametros = urlencode({
            "amount": 10,
            "category": 15,
            "difficulty": dificultad,
            "type": "multiple",
            "encode": "url3986",
        })
        solicitud = Request(
            f"https://opentdb.com/api.php?{parametros}",
            headers={"Accept": "application/json", "User-Agent": "JuegosDjango/1.0"},
        )

        try:
            with urlopen(solicitud, timeout=10) as respuesta:
                datos = json.loads(respuesta.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
            return JsonResponse(
                {"error": "No se pudo conectar con Open Trivia DB."},
                status=503,
            )

        if datos.get("response_code") != 0 or not datos.get("results"):
            return JsonResponse(
                {"error": "La API no encontró preguntas. Intenta con otra dificultad."},
                status=503,
            )

        preguntas = datos["results"]
        cache.set(clave_cache, preguntas, 60 * 30)

    clave_vistas = f"trivia_vistas_{dificultad}"
    ya_vistas = request.session.get(clave_vistas, [])
    disponibles = [p for p in preguntas if p["question"] not in ya_vistas]
    if not disponibles:
        ya_vistas = []
        disponibles = preguntas

    pregunta = random.choice(disponibles)
    ya_vistas.append(pregunta["question"])
    request.session[clave_vistas] = ya_vistas

    decodificar = lambda valor: unquote(valor)
    respuestas = [
        decodificar(valor)
        for valor in [pregunta["correct_answer"], *pregunta["incorrect_answers"]]
    ]
    random.shuffle(respuestas)

    return JsonResponse({
        "categoria": decodificar(pregunta["category"]),
        "dificultad": dificultad,
        "pregunta": decodificar(pregunta["question"]),
        "respuesta_correcta": decodificar(pregunta["correct_answer"]),
        "opciones": respuestas,
    })
