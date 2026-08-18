from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path('auth/register/', views.RegisterAPI.as_view()),
    path('auth/login/', views.LoginAPI.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/me/', views.MeAPI.as_view()),
    path('auth/me/password/', views.ChangePasswordAPI.as_view()),
    path('auth/me/delete/', views.DeleteAccountAPI.as_view()),
    path('auth/membros/', views.MembrosListAPI.as_view()),
    path('auth/membros/nivel/', views.MudarNivelAPI.as_view()),
    path('auth/seguranca/', views.SenhaSegurancaAPI.as_view()),
    # Conteúdo
    path('home/', views.HomeAPI.as_view()),
    path('eventos/', views.EventoListAPI.as_view()),
    path('admin/eventos/', views.EventoAdminAPI.as_view()),
    path('admin/eventos/<int:pk>/', views.EventoDeleteAPI.as_view()),
    path('galeria/', views.GaleriaListAPI.as_view()),
    path('admin/galeria/', views.GaleriaAdminAPI.as_view()),
    path('admin/galeria/<int:pk>/', views.GaleriaDeleteAPI.as_view()),
    path('contacto/', views.MensagemCreateAPI.as_view()),
    path('admin/mensagens/', views.MensagemListAPI.as_view()),
    path('admin/mensagens/<int:pk>/', views.MensagemDeleteAPI.as_view()),
    path('admin/historico/', views.AuditoriaListAPI.as_view()),
    path('admin/alertas/', views.AlertasListAPI.as_view()),
    path('admin/alertas/marcar/', views.AlertaMarcarAPI.as_view()),
]
