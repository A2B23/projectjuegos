from django.urls import path
from . import views

app_name = "juegos_app"

urlpatterns = [
    path("", views.lista_juegos, name="lista"),
    path("juego/<int:pk>/", views.detalle_juego, name="detalle"),
]