# admin.py
from django.contrib import admin
from .models import Alumno, Equipo, Materia

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display   = ("matricula", "apellido_paterno", "apellido_materno", "nombre", "año_de_generacion")
    list_filter    = ("año_de_generacion",)
    search_fields  = ("matricula", "apellido_paterno", "apellido_materno", "nombre")

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display       = ("nombre", "puntos")
    filter_horizontal  = ("alumnos", "materias")

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display      = ("nombre", "codigo")
    search_fields     = ("nombre", "codigo")
