# views.py
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView, DetailView, View
from django.shortcuts import redirect, get_object_or_404
from equipos.models import Alumno, Materia, Equipo
from django.db.models import Sum, F

from generales.forms import AlumnoForm, MateriaForm
from equipos.forms import EquipoForm

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
    form_class = AlumnoForm
    template_name = 'generales/alumno_form.html'
    success_url = reverse_lazy('home')

class MateriaCreateView(LoginRequiredMixin, CreateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'generales/materia_form.html'
    success_url = reverse_lazy('home')

class MateriaListView(LoginRequiredMixin, ListView):
    model = Materia
    context_object_name = 'materias'
    template_name = 'generales/materia_list.html'


class EquipoCreateView(LoginRequiredMixin, CreateView):
    model = Equipo
    form_class = EquipoForm
    template_name = 'generales/equipo_form.html'
    success_url = reverse_lazy('home')


class EquipoListView(LoginRequiredMixin, ListView):
    model = Equipo
    context_object_name = 'equipos'
    template_name = 'generales/equipo_list.html'


class EquipoDetailView(LoginRequiredMixin, DetailView):
    model = Equipo
    context_object_name = 'equipo'
    template_name = 'generales/equipo_detail.html'

class MateriaDetailView(LoginRequiredMixin, DetailView):
    model = Materia
    context_object_name = 'materia'
    template_name = 'generales/materia_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['equipos'] = self.object.equipos.all()
        return ctx


class EquipoAddPointView(LoginRequiredMixin, View):
    def post(self, request, pk):
        Equipo.objects.filter(pk=pk).update(puntos=F('puntos') + 1)
        return redirect('equipo_list')


class EquipoRemovePointView(LoginRequiredMixin, View):
    def post(self, request, pk):
        equipo = get_object_or_404(Equipo, pk=pk)
        if equipo.puntos > 0:
            equipo.puntos -= 1
            equipo.save()
        return redirect('equipo_list')
