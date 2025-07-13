# generales/forms.py
from django import forms
from equipos.models import Actividad, Calificacion, Materia, Alumno, Equipo, SubMateria


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['nombre', 'codigo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Nombre de la materia'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Código (p. ej. MAT101)'
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'codigo': 'Código',
        }

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = [
            'apellido_paterno',
            'apellido_materno',
            'nombre',
            'matricula',
            'año_de_generacion',
        ]
        widgets = {
            'apellido_paterno': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Apellido paterno'
            }),
            'apellido_materno': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Apellido materno'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Nombre(s)'
            }),
            'matricula': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Matrícula (única)'
            }),
            'año_de_generacion': forms.NumberInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Ejemplo: 2021',
                'min': '1900', 'max': '2100'
            }),
        }
        labels = {
            'apellido_paterno': 'Apellido paterno',
            'apellido_materno': 'Apellido materno',
            'nombre': 'Nombre',
            'matricula': 'Matrícula',
            'año_de_generacion': 'Año de generación',
        }
        help_texts = {
            'año_de_generacion': 'Ejemplo: 2021',
        }



# forms.py
from django import forms
from django.forms import inlineformset_factory

from equipos.models import Alumno


class SubMateriaForm(forms.ModelForm):
    class Meta:
        model  = SubMateria
        fields = ("nombre",)
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control",
                                             "placeholder": "Nombre de la sub-materia"})
        }


class ActividadForm(forms.ModelForm):
    class Meta:
        model  = Actividad
        fields = ("titulo", "descripcion", "fecha_entrega", "ponderacion")
        widgets = {
            "titulo":        forms.TextInput(attrs={"class": "form-control"}),
            "descripcion":   forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "fecha_entrega": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "ponderacion":   forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }


# ----- Calificaciones -----
class CalificacionForm(forms.ModelForm):
    class Meta:
        model   = Calificacion
        fields  = ("alumno", "valor")
        widgets = {
            "alumno": forms.Select(attrs={
                "class": "form-select",
            }),
            "valor":  forms.NumberInput(attrs={
                "class": "form-control",
                "step": 0.1,
                "min": 0,
                "max": 10,
            }),
        }

CalificacionFormSet = inlineformset_factory(
    Actividad,
    Calificacion,
    form=CalificacionForm,
    extra=0,
    can_delete=False,
)




