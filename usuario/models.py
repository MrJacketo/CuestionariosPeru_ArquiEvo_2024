from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    foto_perfil= models.ImageField(upload_to='foto_perfil/Usuario',null=True,blank=True)
    direccion = models.CharField(max_length=40)
    celular = models.CharField(max_length=20,null=False)
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name