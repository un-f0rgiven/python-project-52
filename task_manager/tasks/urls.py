from django.urls import path

from task_manager.tasks.views import (
    TaskCreateView,
    TaskDeleteView,
    TaskListView,
    TaskShowView,
    TaskUpdateView,
)

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/', TaskShowView.as_view(), name='task_show'),
]