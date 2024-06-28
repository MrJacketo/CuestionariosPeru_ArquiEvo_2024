from django.urls import path
from usuario import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('usuarioclick', views.usuarioclick_view),
path('usuariologin', LoginView.as_view(template_name='usuario/usuariologin.html'),name='usuariologin'),
path('usuariosignup', views.usuario_signup_view,name='usuariosignup'),
path('usuario_dashboard', views.usuario_dashboard_view,name='usuario_dashboard'),
path('usuario_cuestionario', views.usuario_cuestionario_view,name='usuario_cuestionario'),
path('take-cuestionario/<int:pk>', views.take_cuestionario_view,name='take-cuestionario'),
path('start-cuestionario/<int:pk>', views.start_cuestionario_view,name='start-cuestionario'),

path('calculate-puntajes', views.calculate_puntajes_view,name='calculate-puntajes'),
path('view-resultado', views.view_resultado_view,name='view-resultado'),
path('check-puntajes/<int:pk>', views.check_puntajes_view,name='check-puntajes'),
path('usuario-puntajes', views.usuario_puntajes_view,name='usuario_puntajes'),
]