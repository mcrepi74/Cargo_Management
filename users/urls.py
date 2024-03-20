from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('update/<int:pk>/', views.update, name='update'),
    path('edituser/<int:pk>/', views.edituser, name='edituser'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('makeadmin/<int:pk>/', views.makeadmin, name='makeadmin'),
    path('profile/<int:pk>/', views.details, name='details'),
    path('adduser/', views.adduser, name='adduser'),
]
