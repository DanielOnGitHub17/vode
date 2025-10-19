from django.contrib import admin
from .models import Role, Round, Candidate, Recruiter


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
	list_display = ("title", "num_rounds", "created_at", "updated_at")
	search_fields = ("title", "description")


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
	list_display = ("role", "round_number", "name", "difficulty_level", "time_limit")
	list_filter = ("difficulty_level", "role")
	search_fields = ("name", "description", "data_structures")


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "role", "current_round", "ai_score", "needs_review", "created_at")
	list_filter = ("current_round", "needs_review", "role")
	search_fields = ("name", "email", "notes")


@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
	list_display = ("user", "created_at", "updated_at")
	search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
