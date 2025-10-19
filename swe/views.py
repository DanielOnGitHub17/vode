from django.shortcuts import render, get_object_or_404
from interview.models import Role, Round, Interview
from cand.models import Candidate


def index(request):
    """SWE landing page showing all roles"""
    roles = Role.objects.all()
    return render(request, 'swe/index.html', {'roles': roles})


def role_detail(request, role_id):
    """SWE view for a specific role - shows current round characteristics and candidates needing review"""
    role = get_object_or_404(Role, pk=role_id)
    
    # Get interviews for this role with scores between 70-85 (need manual review)
    interviews = Interview.objects.filter(
        round__role=role, 
        score__gte=70, 
        score__lt=85
    ).order_by('-score').select_related('candidate')
    
    candidates = [interview.candidate for interview in interviews]
    
    # Get the current round (Round 1 by default, or user can specify)
    current_round_num = int(request.GET.get('round', 1))
    if current_round_num > role.num_rounds or current_round_num < 1:
        current_round_num = 1
    
    current_round = role.rounds.filter(round_number=current_round_num).first()
    
    return render(request, 'swe/role_detail_swe.html', {
        'role': role,
        'current_round': current_round,
        'current_round_num': current_round_num,
        'num_rounds': role.num_rounds,
        'candidates': candidates,
    })


def review_candidates(request, role_id):
    """SWE view for candidates who need manual review for a specific role"""
    role = get_object_or_404(Role, pk=role_id)
    
    # Get interviews with scores between 70-85 (not too low, not high enough to pass)
    interviews = Interview.objects.filter(
        round__role=role,
        score__gte=70,
        score__lt=85
    ).order_by('-round__round_number', '-score').select_related('candidate')
    
    candidates = [interview.candidate for interview in interviews]
    
    return render(request, 'swe/review_candidates.html', {
        'role': role,
        'candidates': candidates,
    })
