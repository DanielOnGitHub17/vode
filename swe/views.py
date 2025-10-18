from django.shortcuts import render, get_object_or_404
from recruit.models import Role, Round


def index(request):
    """SWE landing page showing all roles"""
    roles = Role.objects.all()
    return render(request, 'swe/index.html', {'roles': roles})


def role_detail(request, role_id):
    """SWE view for a specific role - shows round configurations"""
    role = get_object_or_404(Role, pk=role_id)
    active_tab = int(request.GET.get('tab', 1))
    
    # Validate tab is within range
    if active_tab > role.num_rounds or active_tab < 1:
        active_tab = 1
    
    all_rounds = role.rounds.all()
    active_round_config = role.rounds.filter(round_number=active_tab).first()
    
    rounds = list(range(1, role.num_rounds + 1))
    
    return render(request, 'swe/role_detail_swe.html', {
        'role': role,
        'active_tab': active_tab,
        'rounds': rounds,
        'active_round_config': active_round_config,
        'all_rounds_config': all_rounds,
    })
