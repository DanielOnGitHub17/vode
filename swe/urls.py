from django.urls import path
from . import views

app_name = 'swe'

urlpatterns = [
    path('', views.index, name='index'),
    path('role/<int:role_id>/rounds/', views.role_rounds, name='role_rounds'),
    path('round/<int:round_id>/edit/', views.round_edit, name='round_edit'),
]
