from django.shortcuts import render, get_object_or_404, redirect
from interview.models import Role, Interview, Round
from cand.models import Candidate


def index(request):
    """Recruiter dashboard - shows all roles"""
    roles = Role.objects.all()
    return render(request, 'recruit/index.html', {'roles': roles})


def role_detail(request, role_id):
    """Recruiter view for a specific role - shows rounds as tiles"""
    role = get_object_or_404(Role, pk=role_id)
    rounds = Round.objects.filter(role=role).order_by('round_number')
    
    return render(request, 'recruit/role_detail.html', {
        'role': role,
        'rounds': rounds
    })


def round_candidates(request, round_id):
    """Recruiter view for a specific round - shows all candidates with scores"""
    round_obj = get_object_or_404(Round, pk=round_id)
    
    # Get all interviews for this round with candidate details
    interviews = Interview.objects.filter(round=round_obj).order_by('-score').select_related('candidate')
    
    return render(request, 'recruit/round_candidates.html', {
        'round': round_obj,
        'role': round_obj.role,
        'interviews': interviews
    })
