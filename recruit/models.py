from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    num_rounds = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Round(models.Model):
    DIFFICULTY_CHOICES = [
        ('very_easy', 'Very Easy'),
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('very_hard', 'Very Hard'),
    ]
    
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='rounds')
    round_number = models.PositiveIntegerField()
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    data_structures = models.TextField(blank=True)
    time_limit = models.PositiveIntegerField(default=30)
    
    class Meta:
        ordering = ['round_number']
        unique_together = ('role', 'round_number')
    
    def __str__(self):
        return f"{self.role.title} - Round {self.round_number}: {self.name}"


class Candidate(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='candidates')
    current_round = models.PositiveIntegerField(default=1)
    ai_score = models.FloatField(default=0.0)
    notes = models.TextField(blank=True)
    needs_review = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.email})"


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='interviewer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Interviewer"
