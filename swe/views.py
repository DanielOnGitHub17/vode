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
    
    current_round_num = int(request.GET.get('round', 1))
    if current_round_num > role.num_rounds or current_round_num < 1:
        current_round_num = 1
    
    current_round = role.rounds.filter(round_number=current_round_num).first()
    
    interviews = Interview.objects.filter(
        round__role=role,
        round__round_number=current_round_num,
        score__gte=70, 
        score__lt=85
    ).order_by('-score').select_related('candidate', 'round')
    
    candidates_for_review = [interview.candidate for interview in interviews]
    
    # Get all rounds for display
    all_rounds = list(role.rounds.all().order_by('round_number'))
    
    return render(request, 'swe/role_detail_swe.html', {
        'role': role,
        'current_round': current_round,
        'current_round_num': current_round_num,
        'num_rounds': role.num_rounds,
        'all_rounds': all_rounds,
        'candidates_for_review': candidates_for_review,
        'has_candidates_to_review': len(candidates_for_review) > 0,
    })

