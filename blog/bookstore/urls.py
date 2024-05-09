
from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home , name="home"),  
    path('book/',views.book , name="book"), 
    # path('customer/',views.customer), 
    path('customer/<str:pk>' , views.customer , name="customer"), 
    path('create/' , views.create, name='create'), 
    path('createOrder/<str:pk>' , views.createOrder, name='createOrder'),
    path('update/<str:pk>' , views.update, name="update") ,
    path('delete/<str:pk>' , views.delete, name= "delete") ,
    path('register/' , views.register , name='regitser') ,
    path('login/' , views.UserLogin, name='login') ,
    path('logout/' , views.userLogout , name='logout'),
    path('user/' , views.userProfile, name='user') ,
    path('profile/' , views.profileInfo, name='profileInfo')
]
