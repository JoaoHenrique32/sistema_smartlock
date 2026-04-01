from django.contrib import admin
from django.urls import path
from camera_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('plataforma/', views.plataforma, name='plataforma'),
    path('dispositivo/', views.dispositivo, name='dispositivo'),
    path('aplicativo/', views.aplicativo, name='aplicativo'),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('identify/', views.identify_face, name='identify_face'),
    path('register/', views.register_face, name='register_face'), # <-- Adicione esta linha
]