from django.db import models


class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "géneros"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Juego(models.Model):
    TIPO_CHOICES = [
        ("instalable", "Para instalar"),
        ("web", "Jugable en la web"),
    ]

    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    imagen = models.URLField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="instalable")
    url = models.URLField(help_text="Web oficial (instalable) o enlace para jugar (web)")
    generos = models.ManyToManyField(Genero, blank=True, related_name="juegos")
    creador = models.CharField(max_length=100, blank=True)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_agregado"]

    def __str__(self):
        return self.titulo