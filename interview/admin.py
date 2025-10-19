from django.contrib import admin
from .models import Interview, Role, Round


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("title", "num_rounds", "assigned_swe", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("num_rounds", "created_at")


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ("role", "round_number", "name", "difficulty_level", "time_limit")
    list_filter = ("difficulty_level", "role")
    search_fields = ("name", "description", "data_structures")


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ("candidate", "round", "score", "completed_at", "created_at")
    list_filter = ("completed_at", "round__role", "score")
    search_fields = ("candidate__user__first_name", "candidate__user__last_name", "notes")

# Register your models here.
