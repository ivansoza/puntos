# forms.py
from django import forms
from django.db.models import Q
from .models import Equipo, Alumno, Materia

class EquipoForm(forms.ModelForm):
    alumnos = forms.ModelMultipleChoiceField(
        queryset=Alumno.objects.none(),
        widget=forms.SelectMultiple(attrs={
            "class": "form-select mb-3 select2",
            "data-placeholder": "Selecciona alumnos…"
        }),
        required=False,
        label="Alumnos"
    )
    materias = forms.ModelMultipleChoiceField(
        queryset=Materia.objects.all(),
        widget=forms.SelectMultiple(attrs={
            "class": "form-select mb-3 select2",
            "data-placeholder": "Selecciona materias…"
        }),
        required=False,
        label="Materias"
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
        labels = {
            "nombre": "Nombre",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si es edición, incluimos los de este equipo + los libres;
        # si es nuevo, sólo los libres.
        if self.instance and self.instance.pk:
            self.fields['alumnos'].queryset = Alumno.objects.filter(
                Q(equipos=None) | Q(equipos=self.instance)
            ).distinct()
        else:
            self.fields['alumnos'].queryset = Alumno.objects.filter(equipos=None)

    def clean_alumnos(self):
        alumnos = self.cleaned_data.get('alumnos', [])
        for alumno in alumnos:
            # equipos distintos al que estamos editando
            otros = alumno.equipos.exclude(pk=self.instance.pk) if self.instance.pk else alumno.equipos.all()
            if otros.exists():
                raise forms.ValidationError(
                    f'El alumno "{alumno}" ya está asignado al equipo “{otros.first()}”.'
                )
        return alumnos
