from django.urls import path
from .views import interview


app_name = "interview"

urlpatterns = [
    path("<int:id>/", interview, name="interview"),
    path("end/<int:id>/", interview, name="end-interview"),
]