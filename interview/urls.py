from django.urls import path
from . import views


app_name = "interview"

urlpatterns = [
    path("<int:id>/", views.interview, name="interview"),
    path("api/question-audio/", views.get_question_audio, name="get_question_audio"),
    path("api/get-response/", views.get_response, name="get_response"),
]