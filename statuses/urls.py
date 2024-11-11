from django.urls import path
from .views import (
    status_list,
    status_create,
    status_update,
    status_delete,
)

urlpatterns = [
    path('', status_list, name='status_list'),
    path('create/', status_create, name='status_create'),
    path('<int:pk>/update/', status_update, name='status_update'),
    path('<int:pk>/delete/', status_delete, name='status_delete'),

]