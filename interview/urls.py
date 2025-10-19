from django.urls import path
from . import views


app_name = "interview"

urlpatterns = [
    path("<int:id>/", views.interview, name="interview"),
    path("api/get-response/", views.get_response, name="get_response"),
    path("api/end-interview/", views.end_interview_audio, name="end_interview_audio"),
]