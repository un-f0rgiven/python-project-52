"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from task_manager.views import index, user_list, user_create, user_update, user_delete, user_login, user_logout

urlpatterns = [
    path('', index),
    path('users/', user_list, name='user_list'),
    path('create/', user_create, name='user_create'),
    path('update/<int:pk>/', user_update, name='user_update'),
    path('delete/<int:pk>/', user_delete, name='user_delete'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('admin/', admin.site.urls),
]
