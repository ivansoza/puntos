from django import forms
from django_select2.forms import ModelSelect2MultipleWidget

from .models import Equipo, Alumno, Materia


class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ["nombre", "alumnos", "materias"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control mb-3",
                "placeholder": "Nombre del equipo"
            }),
            "alumnos": ModelSelect2MultipleWidget(
                model=Alumno,
                search_fields=[
                    "apellido_paterno__icontains",
                    "apellido_materno__icontains",
                    "nombre__icontains",
                ],
                attrs={
                    "class": "form-select mb-3 select2",
                    "data-minimum-input-length": 0,
                },
            ),
            "materias": ModelSelect2MultipleWidget(
                model=Materia,
                search_fields=["nombre__icontains", "codigo__icontains"],
                attrs={
                    "class": "form-select mb-3 select2",
                    "data-minimum-input-length": 0,
                },
            ),
        }
        labels = {
            "nombre": "Nombre",
            "alumnos": "Alumnos",
            "materias": "Materias",
        }