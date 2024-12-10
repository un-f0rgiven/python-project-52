from django.urls import path

from task_manager.users.views import (
    user_create,
    user_delete,
    user_list,
    user_login,
    user_logout,
    user_update,
)

urlpatterns = [
    path('', user_list, name='user_list'),
    path('create/', user_create, name='user_create'),
    path('<int:pk>/update/', user_update, name='user_update'),
    path('<int:pk>/delete/', user_delete, name='user_delete'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
]
