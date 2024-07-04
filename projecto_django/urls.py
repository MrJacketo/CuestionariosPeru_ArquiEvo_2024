from django.urls import path,include
from django.contrib import admin
from cuestionario import views
from django.contrib.auth.views import LogoutView,LoginView

urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('usuario/',include('usuario.urls')),
    
    path('',views.home_view,name=''),
    path('logout', LogoutView.as_view(template_name='componentes/logout.html'),name='logout'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),

    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='cuestionario/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-usuario', views.admin_usuario_view,name='admin-usuario'),
    path('admin-view-usuario', views.admin_view_usuario_view,name='admin-view-usuario'),
    path('admin-view-usuario-puntajes', views.admin_view_usuario_puntajes_view,name='admin-view-usuario-puntajes'),
    path('admin-view-puntajes/<int:pk>', views.admin_view_puntajes_view,name='admin-view-puntajes'),
    path('admin-check-puntajes/<int:pk>', views.admin_check_puntajes_view,name='admin-check-puntajes'),
    path('update-usuario/<int:pk>', views.update_usuario_view,name='update-usuario'),
    path('delete-usuario/<int:pk>', views.delete_usuario_view,name='delete-usuario'),

    path('admin-cuestionario', views.admin_cuestionario_view,name='admin-cuestionario'),
    path('admin-add-cuestionario', views.admin_add_cuestionario_view,name='admin-add-cuestionario'),
    path('admin-view-cuestionario', views.admin_view_cuestionario_view,name='admin-view-cuestionario'),
    path('delete-cuestionario/<int:pk>', views.delete_cuestionario_view,name='delete-cuestionario'),

    path('admin-pregunta', views.admin_pregunta_view,name='admin-pregunta'),
    path('admin-add-pregunta', views.admin_add_pregunta_view,name='admin-add-pregunta'),
    path('admin-view-pregunta', views.admin_view_pregunta_view,name='admin-view-pregunta'),
    path('view-pregunta/<int:pk>', views.view_pregunta_view,name='view-pregunta'),
    path('delete-pregunta/<int:pk>', views.delete_pregunta_view,name='delete-pregunta'),

    path('cuestionarios-ranking/', views.cuestionarios_ranking_view, name='cuestionarios-ranking'),
    path('ranking/<int:cuestionario_id>/', views.ranking_view, name='ranking'),
]