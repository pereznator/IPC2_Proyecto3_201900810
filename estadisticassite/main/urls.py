from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home_view, name='home'),
    path('peticiones', views.peticiones_view, name='peticiones'),
    path('ayuda', views.ayuda_view, name='ayuda'),
]