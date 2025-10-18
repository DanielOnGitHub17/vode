from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('role/<int:role_id>/', views.role_detail, name='role_detail'),
]
