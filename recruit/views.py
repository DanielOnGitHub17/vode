from django.shortcuts import render, get_object_or_404
from .models import Role, Candidate


def index(request):
	roles = Role.objects.all()
	return render(request, 'recruiter/index.html', {'roles': roles})


def role_detail(request, role_id):
	role = get_object_or_404(Role, pk=role_id)
	# Determine which tab/round to show
	tab = int(request.GET.get('tab', 1))
	if tab not in (1, 2, 3):
		tab = 1
	candidates = role.candidates.filter(current_round=tab)
	return render(request, 'recruiter/role_detail.html', {'role': role, 'candidates': candidates, 'active_tab': tab})
