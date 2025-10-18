from django.urls import path
from .views import interview


app_name = "interview"

urlpatterns = [
    path("", interview, name=app_name),
]