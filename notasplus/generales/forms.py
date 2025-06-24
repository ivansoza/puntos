# generales/forms.py
from django import forms
from equipos.models import Materia,Alumno


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