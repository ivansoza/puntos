from django.urls import path
from . import views

urlpatterns = [
    path('',                         views.IndexView.as_view(),        name='home'),
    # Materias...
    path('materias/crear/',          views.MateriaCreateView.as_view(), name='materia_create'),
    path('materias/',                views.MateriaListView.as_view(),   name='materia_list'),
    path('materias/<int:pk>/',       views.MateriaDetailView.as_view(), name='materia_detail'),
    # Alumnos
    path('alumnos/crear/',           views.AlumnoCreateView.as_view(),  name='alumno_create'),
    # Equipos...
    path('equipos/crear/',           views.EquipoCreateView.as_view(),  name='equipo_create'),
    path('equipos/',                 views.EquipoListView.as_view(),    name='equipo_list'),
    path('equipos/<int:pk>/',        views.EquipoDetailView.as_view(),  name='equipo_detail'),
    path('equipos/<int:pk>/add_point/',    views.EquipoAddPointView.as_view(),    name='equipo_add_point'),
    path('equipos/<int:pk>/remove_point/', views.EquipoRemovePointView.as_view(), name='equipo_remove_point'),
]
