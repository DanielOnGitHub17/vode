from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from datetime import datetime, timedelta

from .models import Candidate
from interview.models import Interview

# Create your views here.

class Dashboard(View):
    def get(self, request, *args, **kwargs):
        # Handle GET request
        # TODO: Fetch from database later
        mock_candidate = Candidate.objects.first()  # request.user.candidate
        
        if mock_candidate:
            # Only show interviews that have not been completed
            interviews = Interview.objects.filter(
                candidate=mock_candidate,
                completed_at__isnull=True  # Only pending interviews
            ).select_related(
                "round", "round__role"
            )
        else:
            interviews = Interview.objects.none()

        context = {
            "candidate": mock_candidate,
            "interviews": interviews,
        }

        return render(request, "cand/index.html", context)
    
    def post(self, request, *args, **kwargs):
        # Handle POST request
        return JsonResponse({"status": "success"})