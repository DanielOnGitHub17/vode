from django.shortcuts import render, get_object_or_404
from interview.models import Role, Interview
from cand.models import Candidate


def index(request):
    """Recruiter dashboard - shows all roles"""
    roles = Role.objects.all()
    return render(request, 'recruit/index.html', {'roles': roles})


def role_detail(request, role_id):
    """Recruiter view for a specific role - shows candidates in each round"""
    role = get_object_or_404(Role, pk=role_id)
    active_tab = int(request.GET.get('tab', 1))
    
    if active_tab > role.num_rounds or active_tab < 1:
        active_tab = 1
    
    # Get interviews for this role at the specific round
    interviews = Interview.objects.filter(
        round__role=role,
        round__round_number=active_tab
    ).order_by('-score').select_related('candidate')
    
    candidates = [interview.candidate for interview in interviews]
    rounds = list(range(1, role.num_rounds + 1))
    
    return render(request, 'recruit/role_detail.html', {
        'role': role,
        'candidates': candidates,
        'active_tab': active_tab,
        'rounds': rounds
    })
