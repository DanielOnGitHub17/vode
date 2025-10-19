from django.urls import path
from .views import Dashboard

app_name = "cand"

urlpatterns = [
    path("", Dashboard.as_view(), name="candidate_dashboard"),
]
