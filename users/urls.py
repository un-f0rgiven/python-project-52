from django.urls import path
from .views import user_list, user_create, user_update, user_delete, user_login, user_logout

urlpatterns = [
    path('', user_list, name='user_list'),
    path('create/', user_create, name='user_create'),
    path('<int:pk>/update/', user_update, name='user_update'),
    path('<int:pk>/delete/', user_delete, name='user_delete'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
]