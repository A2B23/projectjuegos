from django.urls import path
from . import views

app_name = "juegos_app"

urlpatterns = [
    path("", views.lista_juegos, name="lista"),
    path("juego/<int:pk>/", views.detalle_juego, name="detalle"),
    path("juego/nuevo/", views.crear_juego, name="crear"),
    path("juegos/<int:pk>/editar/", views.editar_juego, name="editar"),
    path("juegos/<int:pk>/eliminar/", views.eliminar_juego, name="eliminar"),
    path("api/juegos/", views.api_juegos, name="api_juegos"),
    path("trivia/", views.trivia_videojuegos, name="trivia"),
    path("api/trivia/pregunta/", views.api_trivia_pregunta, name="api_trivia_pregunta"),
]
