from django.db import models

class Alumno(models.Model):
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    matricula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.apellido_paterno} {self.apellido_materno} {self.nombre}"

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    alumnos = models.ManyToManyField(Alumno, related_name="equipos", blank=True)
    puntos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre
