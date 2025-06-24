from django.contrib import admin
from .models import Alumno, Equipo

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ("matricula", "apellido_paterno", "apellido_materno", "nombre")
    search_fields = ("matricula", "apellido_paterno", "apellido_materno", "nombre")

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "puntos")
    filter_horizontal = ("alumnos",)
