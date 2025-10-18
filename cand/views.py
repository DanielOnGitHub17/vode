from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from datetime import datetime, timedelta

# Create your views here.

class ActionView(View):
    def get(self, request, *args, **kwargs):
        # Handle GET request
        # TODO: Fetch from database later
        context = {
            'role': {
                'title': 'Senior Software Engineer',
                'description': 'Join our team as a Senior Software Engineer working on cutting-edge cloud infrastructure and distributed systems. You will be responsible for designing and implementing scalable solutions that power millions of users worldwide.',
            },
            'round': {
                'number': 1,
                'start_time': (datetime.now() + timedelta(hours=2)).strftime('%I:%M %p, %B %d, %Y'),
            }
        }
        return render(request, "cand/index.html", context)
    
    def post(self, request, *args, **kwargs):
        # Handle POST request
        return JsonResponse({'status': 'success'})