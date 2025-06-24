from django import forms
from .models import Equipo, Alumno, Materia

class EquipoForm(forms.ModelForm):
    alumnos = forms.ModelMultipleChoiceField(
        queryset=Alumno.objects.all(),
        widget=forms.SelectMultiple(attrs={
          "class": "form-select mb-3 select2",
          "data-placeholder": "Selecciona alumnos…"
        }),
        required=False
    )
    materias = forms.ModelMultipleChoiceField(
        queryset=Materia.objects.all(),
        widget=forms.SelectMultiple(attrs={
          "class": "form-select mb-3 select2",
          "data-placeholder": "Selecciona materias…"
        }),
        required=False
    )
    class Meta:
        model = Equipo
        fields = ["nombre", "alumnos", "materias"]
        widgets = {
          "nombre": forms.TextInput(attrs={
            "class": "form-control mb-3",
            "placeholder": "Nombre del equipo"
          }),
        }
