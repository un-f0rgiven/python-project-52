from django.urls import path
from labels.views import label_list, label_create, label_update, label_delete

urlpatterns = [
    path('labels/', label_list, name='label_list'),
    path('labels/create/', label_create, name='label_create'),
    path('labels/<int:pk>/update/', label_update, name='label_update'),
    path('labels/<int:pk>/delete/', label_delete, name='label_delete'),
]