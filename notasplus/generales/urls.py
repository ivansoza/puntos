from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('dashboard/', views.IndexView.as_view(), name='dashboard'),
    # Materias...
    path('materias/crear/',          views.MateriaCreateView.as_view(), name='materia_create'),
    path('materias/',                views.MateriaListView.as_view(),   name='materia_list'),
    path('materias/<int:pk>/',       views.MateriaDetailView.as_view(), name='materia_detail'),
    # Alumnos
    path('alumnos/crear/',           views.AlumnoCreateView.as_view(),  name='alumno_create'),
    path("alumno/<int:pk>/", views.AlumnoDetailView.as_view(), name="alumno_detail"),
    path("alumno/<int:pk>/editar/", views.AlumnoUpdateView.as_view(), name="alumno_update"),
    path(
        "alumno/<int:alumno_id>/submateria/<int:sub_id>/actividades/",
        views.AlumnoActividadesView.as_view(),
        name="alumno_actividades",
    ),
    # Equipos...
    path('equipos/crear/',           views.EquipoCreateView.as_view(),  name='equipo_create'),
    path('equipos/',                 views.EquipoListView.as_view(),    name='equipo_list'),
    path('equipos/<int:pk>/',        views.EquipoDetailView.as_view(),  name='equipo_detail'),
    path('equipos/<int:pk>/add_point/',    views.EquipoAddPointView.as_view(),    name='equipo_add_point'),
    path('equipos/<int:pk>/remove_point/', views.EquipoRemovePointView.as_view(), name='equipo_remove_point'),
    path(
        'equipo/<int:pk>/cambiar-puntos/<str:action>/',
        views.cambiar_puntos,
        name='equipo_cambiar_puntos'
    ),

    # Sub-materias
    path("materia/<int:materia_id>/subcrear/", views.SubMateriaCreateView.as_view(),
         name="submateria_create"),
    path("submateria/<int:pk>/", views.SubMateriaDetailView.as_view(),
         name="submateria_detail"),

    # Actividades
    path("submateria/<int:submateria_id>/actividad/crear/",
         views.ActividadCreateView.as_view(), name="actividad_create"),

    # Calificaciones
    path("actividad/<int:actividad_id>/calificar/",
         views.CalificacionUpdateView.as_view(), name="calificacion_update"),
]
