from django.shortcuts import render, redirect
from . import forms, models
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from usuario import models as SMODEL
from usuario import forms as SFORM
from django.contrib.auth.models import User

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request, 'cuestionario/index.html')


def is_usuario(user):
    return user.groups.filter(name='USUARIO').exists()


def afterlogin_view(request):
    if is_usuario(request.user):      
        return redirect('usuario/usuario_dashboard')
    else:
        return redirect('admin-dashboard')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict = {
        'total_usuario': SMODEL.Usuario.objects.all().count(),
        'total_cuestionario': models.Cuestionario.objects.all().count(),
        'total_pregunta': models.Pregunta.objects.all().count(),
    }
    return render(request, 'cuestionario/admin_dashboard.html', context=dict)


@login_required(login_url='adminlogin')
def admin_usuario_view(request):
    dict = {
        'total_usuario': SMODEL.Usuario.objects.all().count(),
    }
    return render(request, 'cuestionario/admin_usuario.html', context=dict)


@login_required(login_url='adminlogin')
def admin_view_usuario_view(request):
    usuarios = SMODEL.Usuario.objects.all()
    return render(request, 'cuestionario/admin_view_usuario.html', {'usuarios': usuarios})


@login_required(login_url='adminlogin')
def update_usuario_view(request, pk):
    usuario = SMODEL.Usuario.objects.get(id=pk)
    user = SMODEL.User.objects.get(id=usuario.user_id)
    userForm = SFORM.UsuarioUserForm(instance=user)
    usuarioForm = SFORM.UsuarioForm(request.FILES, instance=usuario)
    mydict = {'userForm': userForm, 'usuarioForm': usuarioForm}
    if request.method == 'POST':
        userForm = SFORM.UsuarioUserForm(request.POST, instance=user)
        usuarioForm = SFORM.UsuarioForm(request.POST, request.FILES, instance=usuario)
        if userForm.is_valid() and usuarioForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            usuarioForm.save()
            return redirect('admin-view-usuario')
    return render(request, 'cuestionario/update_usuario.html', context=mydict)


@login_required(login_url='adminlogin')
def delete_usuario_view(request, pk):
    usuario = SMODEL.Usuario.objects.get(id=pk)
    user = User.objects.get(id=usuario.user_id)
    user.delete()
    usuario.delete()
    return HttpResponseRedirect('/admin-view-usuario')


@login_required(login_url='adminlogin')
def admin_cuestionario_view(request):
    return render(request, 'cuestionario/admin_cuestionario.html')


@login_required(login_url='adminlogin')
def admin_add_cuestionario_view(request):
    cuestionarioForm = forms.CuestionarioFormulario()
    if request.method == 'POST':
        cuestionarioForm = forms.CuestionarioFormulario(request.POST)
        if cuestionarioForm.is_valid():
            cuestionarioForm.save()
        else:
            print("formulario es inválido")
        return HttpResponseRedirect('/admin-view-cuestionario')
    return render(request, 'cuestionario/admin_add_cuestionario.html', {'cuestionarioForm': cuestionarioForm})


@login_required(login_url='adminlogin')
def admin_view_cuestionario_view(request):
    cuestionarios = models.Cuestionario.objects.all()
    return render(request, 'cuestionario/admin_view_cuestionario.html', {'cuestionarios': cuestionarios})


@login_required(login_url='adminlogin')
def delete_cuestionario_view(request, pk):
    cuestionario = models.Cuestionario.objects.get(id=pk)
    cuestionario.delete()
    return HttpResponseRedirect('/admin-view-cuestionario')


@login_required(login_url='adminlogin')
def admin_pregunta_view(request):
    return render(request, 'cuestionario/admin_pregunta.html')


@login_required(login_url='adminlogin')
def admin_add_pregunta_view(request):
    preguntaForm = forms.PreguntaFormulario()
    if request.method == 'POST':
        preguntaForm = forms.PreguntaFormulario(request.POST)
        if preguntaForm.is_valid():
            pregunta = preguntaForm.save(commit=False)
            cuestionario = models.Cuestionario.objects.get(id=request.POST.get('cuestionarioID'))
            pregunta.cuestionario = cuestionario
            pregunta.save()
        else:
            print("formulario es inválido")
        return HttpResponseRedirect('/admin-view-pregunta')
    return render(request, 'cuestionario/admin_add_pregunta.html', {'preguntaForm': preguntaForm})


@login_required(login_url='adminlogin')
def admin_view_pregunta_view(request):
    cuestionarios = models.Cuestionario.objects.all()
    return render(request, 'cuestionario/admin_view_pregunta.html', {'cuestionarios': cuestionarios})


@login_required(login_url='adminlogin')
def view_pregunta_view(request, pk):
    preguntas = models.Pregunta.objects.all().filter(cuestionario_id=pk)
    return render(request, 'cuestionario/view_pregunta.html', {'preguntas': preguntas})


@login_required(login_url='adminlogin')
def delete_pregunta_view(request, pk):
    pregunta = models.Pregunta.objects.get(id=pk)
    pregunta.delete()
    return HttpResponseRedirect('/admin-view-pregunta')


@login_required(login_url='adminlogin')
def admin_view_usuario_puntajes_view(request):
    usuarios = SMODEL.Usuario.objects.all()
    return render(request, 'cuestionario/admin_view_usuario_puntajes.html', {'usuarios': usuarios})


@login_required(login_url='adminlogin')
def admin_view_puntajes_view(request, pk):
    cuestionarios = models.Cuestionario.objects.all()
    respuesta = render(request, 'cuestionario/admin_view_puntajes.html', {'cuestionarios': cuestionarios})
    respuesta.set_cookie('usuario_id', str(pk))
    return respuesta


@login_required(login_url='adminlogin')
def admin_check_puntajes_view(request, pk):
    cuestionario = models.Cuestionario.objects.get(id=pk)
    usuario_id = request.COOKIES.get('usuario_id')
    usuario = SMODEL.Usuario.objects.get(id=usuario_id)
    resultados = models.Resultados.objects.all().filter(cues=cuestionario).filter(usuario=usuario)
    return render(request, 'cuestionario/admin_check_puntajes.html', {'resultados': resultados})


@login_required(login_url='adminlogin')
def ranking_view(request, cuestionario_id):
    cuestionario = models.Cuestionario.objects.get(id=cuestionario_id)
    rankings = SMODEL.Usuario.objects.filter(
        resultados__cues=cuestionario
    ).annotate(
        max_puntaje=Max('resultados__nota')
    ).order_by('-max_puntaje')
    return render(request, 'cuestionario/ranking.html', {'rankings': rankings, 'cuestionario': cuestionario})


@login_required(login_url='adminlogin')
def cuestionarios_ranking_view(request):
    cuestionarios = models.Cuestionario.objects.all()
    return render(request, 'cuestionario/cuestionarios_ranking.html', {'cuestionarios': cuestionarios})
