from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

# Create your views here.

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        # Handle GET request
        context = {}
        return render(request, 'dashboard.html', context)
    
    def post(self, request, *args, **kwargs):
        # Handle POST request
        return JsonResponse({'status': 'success'})