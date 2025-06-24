# modelos.py
from django.db import models

class Materia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=20, blank=True, help_text="Código opcional de la materia")
    
    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    apellido_paterno   = models.CharField(max_length=50)
    apellido_materno   = models.CharField(max_length=50)
    nombre             = models.CharField(max_length=50)
    matricula          = models.CharField(max_length=20, unique=True)
    año_de_generacion  = models.PositiveIntegerField(
        verbose_name="Año de generación",
        help_text="Ejemplo: 2021"
    )

    def __str__(self):
        return f"{self.apellido_paterno} {self.apellido_materno} {self.nombre}"

class Equipo(models.Model):
    nombre    = models.CharField(max_length=100)
    alumnos   = models.ManyToManyField(Alumno, related_name="equipos", blank=True)
    materias  = models.ManyToManyField(Materia, related_name="equipos", blank=True)
    puntos    = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre
