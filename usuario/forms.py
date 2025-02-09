from django import forms
from django.contrib.auth.models import User
from . import models
from cuestionario import models as QMODEL

class UsuarioUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = models.Usuario
        fields = ['direccion', 'celular', 'foto_perfil']

