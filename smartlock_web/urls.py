from django.contrib import admin
from django.urls import path
from camera_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('identify/', views.identify_face, name='identify_face'),
    path('register/', views.register_face, name='register_face'),
    path('delete/', views.delete_face, name='delete_face'),
]