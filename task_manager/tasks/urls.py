from django.urls import path

from .views import task_create, task_delete, task_list, task_show, task_update

urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', task_create, name='task_create'),
    path('<int:pk>/update/', task_update, name='task_update'),
    path('<int:pk>/delete/', task_delete, name='task_delete'),
    path('<int:pk>/', task_show, name='task_show'),
]
