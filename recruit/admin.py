from django.contrib import admin
from .models import Recruiter

@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
	list_display = ("user", "created_at", "updated_at")
	search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
