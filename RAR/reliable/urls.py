from django.urls import path, include
from . import views
app_name = "reliable"
urlpatterns = [
    path('', views.index, name= 'index'),        
    path('pricing/', views.pricing, name= 'pricing'),
    path('register/', views.register, name= 'register'),
    path('logon/', views.logon, name= 'logon'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('service/', views.service, name='service'),
]
