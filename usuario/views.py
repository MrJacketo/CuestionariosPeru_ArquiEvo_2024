from django.shortcuts import render,redirect,reverse, get_object_or_404
from . import forms,models
from django.db.models import Max
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from cuestionario import models as QMODEL


#for showing signup/login button for usuario
def usuarioclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'usuario/usuarioclick.html')

def usuario_signup_view(request):
    userForm=forms.UsuarioUserForm()
    usuarioForm=forms.UsuarioForm()
    mydict={'userForm':userForm,'usuarioForm':usuarioForm}
    if request.method=='POST':
        userForm=forms.UsuarioUserForm(request.POST)
        usuarioForm=forms.UsuarioForm(request.POST,request.FILES)
        if userForm.is_valid() and usuarioForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            usuario=usuarioForm.save(commit=False)
            usuario.user=user
            usuario.save()
            my_usuario_group = Group.objects.get_or_create(name='USUARIO')
            my_usuario_group[0].user_set.add(user)
        return HttpResponseRedirect('usuariologin')
    return render(request,'usuario/usuariosignup.html',context=mydict)

def is_usuario(user):
    return user.groups.filter(name='USUARIO').exists()

@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def usuario_dashboard_view(request):
    dict={
    
    'total_cuestionario':QMODEL.Cuestionario.objects.all().count(),
    'total_pregunta':QMODEL.Pregunta.objects.all().count(),
    }
    return render(request,'usuario/usuario_dashboard.html',context=dict)

@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def usuario_cuestionario_view(request):
    cuestionarios=QMODEL.Cuestionario.objects.all()
    return render(request,'usuario/usuario_cuestionario.html',{'cuestionarios':cuestionarios})

@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def take_cuestionario_view(request,pk):
    cuestionario=QMODEL.Cuestionario.objects.get(id=pk)
    numero_preguntas=QMODEL.Pregunta.objects.all().filter(cuestionario=cuestionario).count()
    preguntas=QMODEL.Pregunta.objects.all().filter(cuestionario=cuestionario)
    puntaje_maximo=0
    for q in preguntas:
        puntaje_maximo=puntaje_maximo + q.puntaje
    
    return render(request,'usuario/take_cuestionario.html',{'cuestionario':cuestionario,'numero_preguntas':numero_preguntas,'puntaje_maximo':puntaje_maximo})

@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def start_cuestionario_view(request,pk):
    cuestionario=QMODEL.Cuestionario.objects.get(id=pk)
    preguntas=QMODEL.Pregunta.objects.all().filter(cuestionario=cuestionario)
    if request.method=='POST':
        pass
    respuesta= render(request,'usuario/start_cuestionario.html',{'cuestionario':cuestionario,'preguntas':preguntas})
    respuesta.set_cookie('cuestionario_id',cuestionario.id)
    return respuesta


@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def calculate_puntajes_view(request):
    if request.COOKIES.get('cuestionario_id') is not None:
        cuestionario_id = request.COOKIES.get('cuestionario_id')
        cuestionario=QMODEL.Cuestionario.objects.get(id=cuestionario_id)
        
        puntaje_maximo=0
        preguntas=QMODEL.Pregunta.objects.all().filter(cuestionario=cuestionario)
        for i in range(len(preguntas)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = preguntas[i].respuesta
            if selected_ans == actual_answer:
                puntaje_maximo = puntaje_maximo + preguntas[i].puntaje
        usuario = models.Usuario.objects.get(user_id=request.user.id)
        resultado = QMODEL.Resultados()
        resultado.nota=puntaje_maximo
        resultado.cues=cuestionario
        resultado.usuario=usuario
        resultado.save()

        return HttpResponseRedirect('view-resultado')



@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def view_resultado_view(request):
    cuestionarios=QMODEL.Cuestionario.objects.all()
    return render(request,'usuario/view_resultado.html',{'cuestionarios':cuestionarios})
    

@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def check_puntajes_view(request,pk):
    cuestionario=QMODEL.Cuestionario.objects.get(id=pk)
    usuario = models.Usuario.objects.get(user_id=request.user.id)
    resultados= QMODEL.Resultados.objects.all().filter(cues=cuestionario).filter(usuario=usuario)
    return render(request,'usuario/check_puntajes.html',{'resultados':resultados})

@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def usuario_puntajes_view(request):
    cuestionarios=QMODEL.Cuestionario.objects.all()
    return render(request,'usuario/usuario_puntajes.html',{'cuestionarios':cuestionarios})
    
@login_required(login_url='login')
def usuario_ranking_view(request):
    cuestionarios = QMODEL.Cuestionario.objects.all()
    return render(request, 'usuario/ranking.html', {'cuestionarios': cuestionarios})

@login_required(login_url='login')
def usuario_ranking_detalle_view(request, cuestionario_id):
    cuestionario = QMODEL.Cuestionario.objects.get(id=cuestionario_id)
    rankings = models.Usuario.objects.filter(
        resultados__cues=cuestionario
    ).annotate(
        max_puntaje=Max('resultados__nota')
    ).order_by('-max_puntaje')
    return render(request, 'usuario/ranking_detalle.html', {'rankings': rankings, 'cuestionario': cuestionario})
  