from django.db import models
from usuario.models import Usuario

class Cuestionario(models.Model):
   nombre_cuestionario = models.CharField(max_length=50)
   descripcion_cuestionario = models.TextField(max_length=350)
   numero_preguntas = models.PositiveIntegerField()
   puntaje_maximo = models.PositiveIntegerField()
   def __str__(self):
        return self.nombre_cuestionario

class Pregunta(models.Model):
    cuestionario=models.ForeignKey(Cuestionario,on_delete=models.CASCADE)
    puntaje=models.PositiveIntegerField()
    pregunta=models.CharField(max_length=600)
    opcion1=models.CharField(max_length=200)
    opcion2=models.CharField(max_length=200)
    opcion3=models.CharField(max_length=200)
    opcion4=models.CharField(max_length=200)
    cat=(('Opcion1','Opcion1'),('Opcion2','Opcion2'),('Opcion3','Opcion3'),('Opcion4','Opcion4'))
    respuesta=models.CharField(max_length=200,choices=cat)

class Resultados(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    cues = models.ForeignKey(Cuestionario,on_delete=models.CASCADE)
    nota = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now=True)

class Ranking(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntaje_total = models.PositiveIntegerField(default=0)