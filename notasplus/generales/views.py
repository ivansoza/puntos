# views.py
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from equipos.models import Alumno, Materia, Equipo
from django.db.models import Sum

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'generales/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['materias'] = Materia.objects.all()
        # Anotamos a cada alumno la suma de puntos de sus equipos
        ctx['alumnos'] = (
            Alumno.objects
                  .annotate(total_points=Sum('equipos__puntos'))
                  .prefetch_related('equipos')
        )
        return ctx
class AlumnoCreateView(LoginRequiredMixin, CreateView):
    model = Alumno
    fields = ['apellido_paterno', 'apellido_materno', 'nombre', 'matricula', 'año_de_generacion']
    template_name = 'generales/alumno_form.html'
    success_url = reverse_lazy('home')

class MateriaCreateView(LoginRequiredMixin, CreateView):
    model = Materia
    fields = ['nombre', 'codigo']
    template_name = 'generales/materia_form.html'
    success_url = reverse_lazy('home')


class MateriaListView(LoginRequiredMixin, ListView):
    model = Materia
    context_object_name = 'materias'
    template_name = 'generales/materia_list.html'


class EquipoCreateView(LoginRequiredMixin, CreateView):
    model = Equipo
    fields = ['nombre', 'alumnos', 'materias']
    template_name = 'generales/equipo_form.html'
    success_url = reverse_lazy('home')


class EquipoListView(LoginRequiredMixin, ListView):
    model = Equipo
    context_object_name = 'equipos'
    template_name = 'generales/equipo_list.html'

class MateriaDetailView(LoginRequiredMixin, DetailView):
    model = Materia
    context_object_name = 'materia'
    template_name = 'generales/materia_detail.html'