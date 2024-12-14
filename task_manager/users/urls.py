from django.urls import path

from task_manager.users.views import (
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserLoginView,
    UserLogoutView,
    UserUpdateView,
)

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
]
