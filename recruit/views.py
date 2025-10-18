from django.shortcuts import render, get_object_or_404
from .models import Role, Candidate


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
    candidates = role.candidates.filter(current_round=active_tab)
    rounds = list(range(1, role.num_rounds + 1))
    
    return render(request, 'recruit/role_detail.html', {
        'role': role,
        'candidates': candidates,
        'active_tab': active_tab,
        'rounds': rounds
    })
