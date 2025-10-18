from django.urls import path
from .views import ActionView

app_name = "cand"

urlpatterns = [
    path("action/", ActionView.as_view(), name="action"),
]