from django.urls import path
from . import views

urlpatterns = [
    path('tareas', views.tareas, name='mis_tareas'),
]