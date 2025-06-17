from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='task-list'),
    # path('add/', views.add_task, name='add-task'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
]
