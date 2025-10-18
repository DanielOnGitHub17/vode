from django.db import models
from django.contrib.auth.models import User

class SWE(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='swe')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - SWE"

