from django.shortcuts import render, get_object_or_404, redirect
from .models import Juego, Genero
from .froms import JuegoForm
from django.shortcuts import redirect
from django.contrib import messages

def crear_juego(request):
    form = JuegoForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Juego creado correctamente.")
        return redirect("juegos_app:lista")  

    return render(request, "crear_juego.html", {"form": form})


def lista_juegos(request):
    tipo = request.GET.get("tipo")
    juegos = Juego.objects.prefetch_related("generos")
    if tipo in ("instalable", "web"):
        juegos = juegos.filter(tipo=tipo)
    return render(request, "juegos_app/lista.html", {"juegos": juegos, "tipo": tipo})


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

        
        