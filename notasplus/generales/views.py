# views.py
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView, DetailView, View
from django.shortcuts import redirect, get_object_or_404
from equipos.models import Actividad, Alumno, Calificacion, Materia, Equipo, SubMateria
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, FormView
from django.db.models import Count, Avg
from django.db.models import Sum, Prefetch
from django.views.generic import UpdateView

from generales.forms import ActividadForm, AlumnoForm, CalificacionFormSet, MateriaForm, SubMateriaForm
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
    model               = Materia
    context_object_name = "materia"
    template_name       = "generales/materia_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # ① Ranking de equipos (lo que ya tenías)
        ctx["equipos"] = (
            self.object.equipos
                      .all()
                      .order_by("-puntos", "nombre")
        )

        # ② Lista de sub-materias con nº de actividades
        ctx["submaterias"] = (
            self.object.submaterias
                      .annotate(total_actividades=Count("actividades"))
                      .order_by("nombre")
        )
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


@login_required
def cambiar_puntos(request, pk, action):
    equipo = get_object_or_404(Equipo, pk=pk)
    # Sumar o restar
    if action == 'sumar':
        equipo.puntos += 1
        texto = f"+1 punto a «{equipo.nombre}»"
    elif action == 'restar':
        if equipo.puntos > 0:
            equipo.puntos -= 1
            texto = f"-1 punto a «{equipo.nombre}»"
        else:
            messages.error(request, f"{equipo.nombre} ya está en 0 puntos.")
            return redirect(request.META.get('HTTP_REFERER', 'home'))
    else:
        messages.error(request, "Acción inválida.")
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    equipo.save()
    messages.success(request, texto)
    # Volver a la misma página
    return redirect(request.META.get('HTTP_REFERER', 'home'))



class SubMateriaCreateView(LoginRequiredMixin, CreateView):
    model         = SubMateria
    form_class    = SubMateriaForm
    template_name = "generales/submateria_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.materia = get_object_or_404(Materia, pk=kwargs["materia_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.materia = self.materia
        messages.success(self.request, "Sub-materia creada con éxito.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("materia_detail", args=[self.materia.pk])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["materia"] = self.materia
        return ctx


# ───────────────────────── 2) Detalle Sub-materia ──────────────────────
class SubMateriaDetailView(LoginRequiredMixin, DetailView):
    model               = SubMateria
    context_object_name = "submateria"
    template_name       = "generales/submateria_detail.html"

    # … (get_queryset sin cambios) …

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        sub = self.object

        # 1) Actividades
        ctx["actividades"] = (
            sub.actividades
               .all()
               .prefetch_related("calificaciones")
               .order_by("fecha_entrega")
        )

        # 2) Alumnos de la materia
        alumnos = (
            Alumno.objects
                  .filter(equipos__materias=sub.materia)
                  .distinct()
                  .order_by("apellido_paterno", "apellido_materno", "nombre")
        )

        total_acts = sub.total_actividades() or 1  # evita división 0

        # 3) Suma de calificaciones por alumno (UNA query)
        # 3) Suma de calificaciones por alumno (UNA query)
        sumas = (
            Calificacion.objects
                .filter(actividad__submateria=sub)
                .values("alumno")
                .annotate(suma=Sum("valor"))
        )

        # ─── DEBUG: imprime qué llegó realmente ───
        print("=== DEBUG → Calificaciones recuperadas ===")
        for fila in sumas:
            alumno_id = fila["alumno"]
            total     = fila["suma"]
            print(f"Alumno ID {alumno_id}: suma = {total}")
        print("=== FIN DEBUG ============================")
        sumas_map = {x["alumno"]: x["suma"] for x in sumas}
        # 4) Promedios
        promedios = {
            al.id: (sumas_map.get(al.id, 0) / total_acts)
            for al in alumnos
        }

        ctx["alumnos"]   = alumnos
        ctx["promedios"] = promedios
        return ctx

# ───────────────────────── 3) Crear Actividad ──────────────────────────
class ActividadCreateView(LoginRequiredMixin, CreateView):
    model         = Actividad
    form_class    = ActividadForm
    template_name = "generales/actividad_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.submateria = get_object_or_404(SubMateria, pk=kwargs["submateria_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.submateria = self.submateria
        messages.success(self.request, "Actividad creada correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("submateria_detail", args=[self.submateria.pk])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["submateria"] = self.submateria
        return ctx


# ─────────────────────── 4) Asignar / Editar Calificaciones ────────────
class CalificacionUpdateView(LoginRequiredMixin, FormView):
    template_name = "generales/calificacion_formset.html"
    form_class    = CalificacionFormSet
    login_url     = "login"

    # 1) Localizamos la actividad una sola vez
    def dispatch(self, request, *args, **kwargs):
        self.actividad = get_object_or_404(Actividad, pk=kwargs["actividad_id"])
        return super().dispatch(request, *args, **kwargs)

    # 2) Inyectamos la instancia (Actividad) al formset
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.actividad

        # Cuando NO existan calificaciones, creamos filas por cada alumno
        if (self.request.method == "GET"
            and not self.actividad.calificaciones.exists()):
            alumnos = (
                Alumno.objects
                      .filter(equipos__materias=self.actividad.submateria.materia)
                      .distinct()
            )
            for alumno in alumnos:
                Calificacion.objects.get_or_create(
                    actividad=self.actividad,
                    alumno=alumno,
                    defaults={"valor": 0.0},
                )
        return kwargs

    # 3) Guardamos y redirigimos
    def form_valid(self, form):
        form.save()                            # ← ¡Aquí se actualiza todo!
        messages.success(self.request, "Calificaciones guardadas.")
        return redirect(
            "submateria_detail",
            self.actividad.submateria.pk
        )

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Hay errores en una o más calificaciones. Revísalas."
        )
        return super().form_invalid(form)

    # 4) Contexto extra
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["formset"]    = ctx["form"]          # alias para la plantilla
        ctx["actividad"]  = self.actividad
        ctx["submateria"] = self.actividad.submateria
        return ctx
    



class AlumnoDetailView(LoginRequiredMixin, DetailView):
    model         = Alumno
    template_name = "generales/alumno_detail.html"

    def get_queryset(self):
        return (
            Alumno.objects
                  .annotate(total_points=Sum("equipos__puntos"))
                  .prefetch_related(
                      Prefetch("equipos",
                               queryset=Equipo.objects.prefetch_related("materias"))
                  )
        )

    def get_context_data(self, **kwargs):
        ctx    = super().get_context_data(**kwargs)
        alumno = self.object

        materia_info = []

        # 1) Recorremos todas las materias donde el alumno tiene algún equipo
        for mat in {m for eq in alumno.equipos.all() for m in eq.materias.all()}:

            # 2) Equipos del alumno en esa materia
            equipos_en_materia = [
                eq for eq in alumno.equipos.all() if mat in eq.materias.all()
            ]

            # 3) Para cada sub-materia, contamos entregadas / total
            sub_stats = []
            for sub in mat.submaterias.all():
                total       = sub.total_actividades()
                entregadas  = (Calificacion.objects
                               .filter(actividad__submateria=sub, alumno=alumno)
                               .count())
                sub_stats.append({
                    "sub":        sub,
                    "entregadas": entregadas,
                    "total":      total,
                })

            materia_info.append({
                "materia":   mat,
                "equipos":   equipos_en_materia,
                "promedio":  alumno.promedio_materia(mat),
                "sub_stats": sub_stats,
            })

        ctx["materia_info"] = materia_info
        return ctx

class AlumnoUpdateView(LoginRequiredMixin, UpdateView):
    model         = Alumno
    form_class    = AlumnoForm
    template_name = "generales/alumno_update.html"

    def form_valid(self, form):
        messages.success(self.request, "Alumno actualizado correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        # Tras guardar, vuelve a la vista de detalle
        return reverse("alumno_detail", kwargs={"pk": self.object.pk})
    




class AlumnoActividadesView(LoginRequiredMixin, TemplateView):
    template_name = "generales/alumno_actividades.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        alumno      = get_object_or_404(Alumno, pk=self.kwargs["alumno_id"])
        submateria  = get_object_or_404(
            SubMateria,
            pk=self.kwargs["sub_id"],
            materia__equipos__alumnos=alumno,   # opcional: asegura relación
        )

        # Prefetch calificaciones para evitar N+1
        actividades = (Actividad.objects
                       .filter(submateria=submateria)
                       .prefetch_related(
                           Prefetch(
                               "calificaciones",
                               queryset=Calificacion.objects.filter(alumno=alumno),
                               to_attr="calificacion_del_alumno",
                           )
                       )
                       .order_by("fecha_entrega"))

        ctx.update({
            "alumno":      alumno,
            "submateria":  submateria,
            "actividades": actividades,
        })
        return ctx