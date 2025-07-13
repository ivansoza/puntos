# admin.py
from django.contrib import admin
from django.db.models import Count, Avg
from .models import (
    Alumno, Equipo, Materia,
    SubMateria, Actividad, Calificacion
)

# ──────────── Inlines ────────────
class SubMateriaInline(admin.TabularInline):
    model  = SubMateria
    extra  = 1
    fields = ("nombre",)
    show_change_link = True


class ActividadInline(admin.TabularInline):
    model  = Actividad
    extra  = 1
    fields = ("titulo", "fecha_entrega", "ponderacion")
    show_change_link = True


class CalificacionInline(admin.TabularInline):
    model               = Calificacion
    autocomplete_fields = ("alumno",)
    extra               = 0

    # Solo mostramos lo que realmente se puede editar
    fields              = ("alumno", "valor", "fecha_registro")
    readonly_fields     = ("fecha_registro",)   # ← aquí la magia

    ordering            = ("alumno__apellido_paterno",
                           "alumno__apellido_materno",
                           "alumno__nombre")
    can_delete          = False                 # opcional: evita borrar notas
# ──────────── Materia ────────────
@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display        = ("nombre", "codigo", "submaterias_cnt", "promedio_general")
    search_fields       = ("nombre", "codigo")
    inlines             = (SubMateriaInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (qs
                .annotate(_cnt=Count("submaterias", distinct=True))
                .annotate(_prom=Avg("submaterias__actividades__calificaciones__valor")))

    def submaterias_cnt(self, obj):
        return getattr(obj, "_cnt", 0)
    submaterias_cnt.short_description = "Sub-materias"

    def promedio_general(self, obj):
        prom = getattr(obj, "_prom", None) or 0
        return f"{prom:.2f}"
    promedio_general.short_description = "Prom. global"


# ──────────── SubMateria ────────────
@admin.register(SubMateria)
class SubMateriaAdmin(admin.ModelAdmin):
    list_display        = ("nombre", "materia", "total_actividades")
    list_filter         = ("materia",)
    search_fields       = ("nombre", "materia__nombre")
    inlines             = (ActividadInline,)

    def total_actividades(self, obj):
        return obj.total_actividades()
    total_actividades.short_description = "Actividades"


# ──────────── Actividad ────────────
@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display        = (
        "titulo", "submateria", "materia", "fecha_entrega",
        "ponderacion", "calificaciones_cnt"
    )
    list_filter         = ("submateria__materia", "submateria", "fecha_entrega")
    search_fields       = (
        "titulo", "submateria__nombre", "submateria__materia__nombre"
    )
    autocomplete_fields = ("submateria",)
    inlines             = (CalificacionInline,)
    date_hierarchy      = "fecha_entrega"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("submateria", "submateria__materia")\
                 .annotate(_cnt=Count("calificaciones", distinct=True))

    def materia(self, obj):
        return obj.submateria.materia
    materia.admin_order_field = "submateria__materia__nombre"

    def calificaciones_cnt(self, obj):
        return getattr(obj, "_cnt", 0)
    calificaciones_cnt.short_description = "Calif."


# ──────────── Calificacion ────────────
@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display        = ("alumno", "actividad", "valor", "fecha_registro")
    list_editable       = ("valor",)                      # ← edición en línea
    list_filter         = (
        "actividad",                         # actividad puntual
        "actividad__submateria",             # sub-materia
        "actividad__submateria__materia",    # materia
        "alumno__equipos",                   # equipo / grupo
    )
    search_fields       = (
        "alumno__matricula", "alumno__nombre",
        "alumno__apellido_paterno", "actividad__titulo"
    )
    autocomplete_fields = ("alumno", "actividad")
    date_hierarchy      = "fecha_registro"
    list_select_related = ("alumno", "actividad")         # rendimiento
    save_on_top         = True              
# ──────────── Alumno ────────────
@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display   = (
        "matricula", "apellido_paterno",
        "apellido_materno", "nombre", "año_de_generacion"
    )
    list_filter    = ("año_de_generacion",)
    search_fields  = (
        "matricula", "apellido_paterno",
        "apellido_materno", "nombre"
    )
    inlines        = (CalificacionInline,)


# ──────────── Equipo ────────────
@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display       = ("nombre", "puntos")
    filter_horizontal  = ("alumnos", "materias")
    search_fields      = ("nombre",)
