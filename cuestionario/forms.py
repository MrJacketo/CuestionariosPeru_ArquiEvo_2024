from django import forms
from django.contrib.auth.models import User
from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

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
        model = models.Pregunta  # Usa el modelo Pregunta importado correctamente
        fields = ['puntaje', 'pregunta', 'opcion1', 'opcion2', 'opcion3', 'opcion4', 'respuesta']
        widgets = {
            'pregunta': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }
