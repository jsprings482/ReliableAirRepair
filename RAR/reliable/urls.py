from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),        
    path('pricing/', views.pricing, name='pricing'),
    path('register/', views.register, name= 'register'),
    path('logon/', views.logon, name= 'logon'),
    path('logout/', views.logout, name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
]
