# models.py
from django.db import models
from django.db.models import Avg, Count
from django.db.models import Avg, Count, Sum   #  ← añade Sum

# ──────────────────── Materias y Submaterias ────────────────────
class Materia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(
        max_length=20, blank=True,
        help_text="Código opcional de la materia"
    )

    def __str__(self):
        return self.nombre

    # — Promedio general de todos los alumnos en la materia —
    def promedio_general(self):
        return (Calificacion.objects
                .filter(actividad__submateria__materia=self)
                .aggregate(prom=Avg("valor"))["prom"]) or 0


class SubMateria(models.Model):
    materia = models.ForeignKey(
        Materia, on_delete=models.CASCADE, related_name="submaterias"
    )
    nombre = models.CharField(max_length=100)

    class Meta:
        unique_together = ("materia", "nombre")
        verbose_name = "Sub-materia"
        verbose_name_plural = "Sub-materias"

    def __str__(self):
        return f"{self.materia} – {self.nombre}"

    # — Utilidades —
    def total_actividades(self) -> int:
        return self.actividades.count()

    def promedio_alumno(self, alumno):
        """
        Promedio de un alumno en esta sub-materia tomando TODAS las
        actividades. Las que no tengan calificación valen 0.
        """
        total = self.total_actividades()
        if total == 0:
            return 0

        suma = (Calificacion.objects
                .filter(actividad__submateria=self, alumno=alumno)
                .aggregate(total=Sum("valor"))["total"] or 0)

        return suma / total
    def porcentaje_entregado(self, alumno):
        total = self.total_actividades()
        if total == 0:
            return 0
        entregadas = Calificacion.objects.filter(
            actividad__submateria=self, alumno=alumno
        ).count()
        return entregadas / total * 100


# ──────────────────── Actividades y Calificaciones ───────────────
class Actividad(models.Model):
    submateria = models.ForeignKey(
        SubMateria, on_delete=models.CASCADE, related_name="actividades"
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_asignacion = models.DateField(auto_now_add=True)
    fecha_entrega = models.DateField()
    ponderacion = models.PositiveSmallIntegerField(
        default=1,
        help_text="Peso relativo en el cálculo del promedio"
    )

    class Meta:
        ordering = ("fecha_entrega",)

    def __str__(self):
        return f"{self.submateria} | {self.titulo}"


class Calificacion(models.Model):
    actividad = models.ForeignKey(
        Actividad, on_delete=models.CASCADE, related_name="calificaciones"
    )
    alumno = models.ForeignKey(
        "Alumno", on_delete=models.CASCADE, related_name="calificaciones"
    )
    valor = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="Ej.: 8.5, 10.0"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("actividad", "alumno")
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"

    def __str__(self):
        return f"{self.alumno} – {self.actividad}: {self.valor}"


# ──────────────────── Alumnos y Equipos ──────────────────────────
class Alumno(models.Model):
    apellido_paterno  = models.CharField(max_length=50)
    apellido_materno  = models.CharField(max_length=50)
    nombre            = models.CharField(max_length=50)
    matricula         = models.CharField(max_length=20, unique=True)
    año_de_generacion = models.PositiveIntegerField(
        verbose_name="Año de generación",
        help_text="Ejemplo: 2021"
    )

    def __str__(self):
        return f"{self.apellido_paterno} {self.apellido_materno} {self.nombre}"

    # — Ayudas para consultas rápidas —
    def promedio_submateria(self, submateria):
        return submateria.promedio_alumno(self)

    def porcentaje_submateria(self, submateria):
        return submateria.porcentaje_entregado(self)

    def promedio_materia(self, materia):
        """Promedio ponderado del alumno en toda la materia."""
        qs = (Calificacion.objects
              .filter(actividad__submateria__materia=materia, alumno=self)
              .annotate(peso=models.F("actividad__ponderacion")))
        total_peso = qs.aggregate(sum=Count("peso"))["sum"] or 0
        if total_peso == 0:
            return 0
        suma = sum(c.valor * c.actividad.ponderacion for c in qs)
        return suma / total_peso


class Equipo(models.Model):
    nombre   = models.CharField(max_length=100)
    alumnos  = models.ManyToManyField(
        Alumno, related_name="equipos", blank=True
    )
    materias = models.ManyToManyField(
        Materia, related_name="equipos", blank=True
    )
    puntos   = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre
