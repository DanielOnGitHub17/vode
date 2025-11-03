from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from interview.models import Role, Round, Interview
from cand.models import Candidate

# Later, have "additional details, or interviewer behaviour as a setting for swe"

def index(request):
    """SWE landing page showing all roles"""
    roles = Role.objects.prefetch_related("rounds").all()

    return render(request, "swe/index.html", {"roles": roles})


def role_rounds(request, role_id):
    """SWE view to see all rounds for a specific role as tiles"""
    role = get_object_or_404(Role, pk=role_id)
    rounds = role.rounds.all().order_by("round_number")

    return render(request, "swe/role_rounds.html", {"role": role, "rounds": rounds})


def role_detail(request, role_id):
    """SWE view for a specific role - shows current round characteristics and candidates needing review"""
    role = get_object_or_404(Role, pk=role_id)

    current_round_num = int(request.GET.get("round", 1))
    if current_round_num > role.num_rounds or current_round_num < 1:
        current_round_num = 1

    current_round = role.rounds.filter(round_number=current_round_num).first()

    interviews = (
        Interview.objects.filter(
            round__role=role,
            round__round_number=current_round_num,
            score__gte=70,
            score__lt=85,
        )
        .order_by("-score")
        .select_related("candidate", "round")
    )

    candidates_for_review = [interview.candidate for interview in interviews]

    # Get all rounds for display
    all_rounds = list(role.rounds.all().order_by("round_number"))

    return render(
        request,
        "swe/role_detail_swe.html",
        {
            "role": role,
            "current_round": current_round,
            "current_round_num": current_round_num,
            "num_rounds": role.num_rounds,
            "all_rounds": all_rounds,
            "candidates_for_review": candidates_for_review,
            "has_candidates_to_review": len(candidates_for_review) > 0,
        },
    )


@require_http_methods(["GET", "POST"])
def round_edit(request, round_id):
    """SWE view to edit round configuration properties"""
    round_obj = get_object_or_404(Round, pk=round_id)

    if request.method == "POST":
        # Update round properties
        round_obj.name = request.POST.get("name", round_obj.name)
        round_obj.description = request.POST.get("description", round_obj.description)
        round_obj.difficulty_level = request.POST.get(
            "difficulty_level", round_obj.difficulty_level
        )
        round_obj.time_limit = int(request.POST.get("time_limit", round_obj.time_limit))
        round_obj.data_structures = request.POST.get(
            "data_structures", round_obj.data_structures
        )
        round_obj.success_metrics = request.POST.get(
            "success_metrics", round_obj.success_metrics
        )

        round_obj.save()

        return redirect("swe:role_rounds", role_id=round_obj.role.id)

    difficulty_choices = Round.DIFFICULTY_CHOICES

    return render(
        request,
        "swe/round_edit.html",
        {
            "round": round_obj,
            "role": round_obj.role,
            "difficulty_choices": difficulty_choices,
        },
    )
