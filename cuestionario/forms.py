from django import forms
from . import models

class CuestionarioFormulario(forms.ModelForm):
    class Meta:
        model=models.Cuestionario
        fields=['nombre_cuestionario', 'descripcion_cuestionario','numero_preguntas','puntaje_maximo']

class PreguntaFormulario(forms.ModelForm):
    cuestionarioID = forms.ModelChoiceField(
        queryset=models.Cuestionario.objects.all(),
        empty_label="Nombre de Cuestionario",
        to_field_name="id"
    )

    class Meta:
        model = models.Pregunta  
        fields = ['puntaje', 'pregunta', 'opcion1', 'opcion2', 'opcion3', 'opcion4', 'respuesta']
        widgets = {
            'pregunta': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }
