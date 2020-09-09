from django.contrib import admin
from django.urls import path
from . import views


urlpatterns =[
    path('',views.delivery , name='delivery'),
    path('orderdetails/<int:id>/', views.orderdetails, name='orderDetails'),
    path('profile', views.profile, name='profile'),
     path('updateprofile', views.updateprofile, name='updateprofile'),

]
