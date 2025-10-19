from django.urls import path
from . import views

app_name = 'recruit'

urlpatterns = [
    path('', views.index, name='index'),
    path('role/<int:role_id>/', views.role_detail, name='role_detail'),
    path('round/<int:round_id>/candidates/', views.round_candidates, name='round_candidates'),
]
