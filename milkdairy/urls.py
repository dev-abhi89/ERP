"""milk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.dashboard, name ='dashboard'),
    path('logout/',views.logout, name='logout'),
    path('database', views.databse, name='database'),
    path('analytic', views.analytic, name='analytics'),
    path('hubdetail', views.hubdetails, name='hubDetails'),
    path('hublist', views.hublist, name='hubList'),
    path('membership', views.membership, name='memberShip'),
    path('test', views.test, name='lol'),
    path('membership/<int:month>',views.filterMonth, name="filterByMonth"),
    path('membership/<int:month>/<int:day>', views.filterDay, name = 'filterByDay'),

]
