from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('', views.index, name='admin'),
    path('create', views.create, name='create'),
    path('delete', views.delete, name='delete'),
    path('edit', views.edit, name='edit'),
    path('logging', views.logging, name='logging'),
]