from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
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
        # Handle POST request to start interview
        interview_id = request.POST.get("interview_id")
        mock_candidate = Candidate.objects.first()  # TODO: request.user.candidate
        
        if not interview_id:
            messages.error(request, "No interview ID provided.")
            return redirect("/candidate/")

        try:
            interview = Interview.objects.get(id=interview_id)
            
            # Security validation: Verify interview belongs to this candidate
            if interview.candidate != mock_candidate:
                messages.error(request, "You are not authorized to start this interview.")
                return redirect("/candidate/")
            
            # Verify interview hasn't been completed
            if interview.completed_at is not None:
                messages.warning(request, "This interview has already been completed.")
                return redirect("/candidate/")
            
            # Verify interview hasn't already been started
            if interview.started_at is not None:
                # should this not go to the interview?
                messages.warning(request, "This interview has already been started.")
                return redirect("/candidate/")
            
            # Set started_at timestamp
            interview.started_at = timezone.now()
            interview.save()

            # Redirect to interview page with interview ID
            return redirect(f"/interview/{interview.id}/")
        except Interview.DoesNotExist:
            messages.error(request, "Interview not found.")
            return redirect("/candidate/")
