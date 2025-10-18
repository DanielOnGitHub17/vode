from django.contrib import admin
from .models import Role, Round, Candidate


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'num_rounds', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'num_rounds')


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('role', 'round_number', 'name', 'difficulty_level', 'time_limit', 'max_score')
    search_fields = ('name', 'role__title')
    list_filter = ('difficulty_level', 'role')
    ordering = ('role', 'round_number')


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role', 'current_round', 'ai_score', 'needs_review', 'created_at')
    search_fields = ('name', 'email', 'role__title')
    list_filter = ('role', 'current_round', 'needs_review', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Candidate Info', {'fields': ('name', 'email')}),
        ('Role & Round', {'fields': ('role', 'current_round')}),
        ('Evaluation', {'fields': ('ai_score', 'needs_review', 'notes')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
