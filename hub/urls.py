
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name= 'registerForm'),
    path('login', views.login ),
    path('home', views.index, name= 'dashboard' ),


]
