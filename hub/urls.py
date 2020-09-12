
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name= 'registerForm'),
    path('login', views.login ),
    path('home', views.index, name= 'dashboard' ),
    path('profile', views.profile, name = 'profile'),
    path(r'^search/$', views.search, name='hubsearch'),
    path('update/<int:id>', views.orderupdate, name='orderupdate'),
    path('orders', views.membership, name='memberShip'),
    path('orders/<int:month>',views.filterMonth, name="filterByMonth"),
    path('orders/<int:month>/<int:day>', views.filterDay, name = 'filterByDay'),
    path('user/<int:id>/', views.userdetail, name='userDetail'),
    path('d-order/<int:id>/<int:uid>', views.orderdelete, name="deleteorder"),
    path('user-data', views.databse, name='user-database'),
    path('newuser', views.newuser, name = 'newuser'),
    path('deliverylist', views.deliverylist, name='deliverylist'),
    path('delivery-detail/<int:id>', views.deliverydetail, name='delivery-details'),
    path('un-confirmed', views.undefined, name='un-confirmed'),
    path('profile-update', views.profileupdate, name="profile-update"),


]
