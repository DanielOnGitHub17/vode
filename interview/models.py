from django.db import models

from cand.models import Candidate
from recruit.models import Recruiter
from swe.models import SWE

class Role(models.Model):
    """Represents a job role with multiple interview rounds"""
    title = models.CharField(max_length=200, help_text="Job title (e.g., Backend Engineer)")
    description = models.TextField(blank=True, help_text="Role description and responsibilities")
    num_rounds = models.PositiveIntegerField(
        default=3,
        help_text="Number of interview rounds for this role"
    )
    owning_recruiter = models.ForeignKey(Recruiter, on_delete=models.SET_NULL, null=True, blank=False, related_name="owning_recruiter")
    assigned_swe = models.ForeignKey(SWE, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_roles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return f"{self.title} ({self.num_rounds} rounds)"

class Round(models.Model):
    """Represents a single interview round for a role"""
    DIFFICULTY_CHOICES = [
        ('very_easy', 'Very Easy'),
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('very_hard', 'Very Hard'),
    ]

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='rounds')
    round_number = models.PositiveIntegerField(help_text="Round number (1, 2, 3, etc.)")
    name = models.CharField(max_length=200, help_text="Round name (e.g., Coding Challenge)")
    description = models.TextField(blank=True, help_text="Description of the round")
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    data_structures = models.TextField(blank=True, help_text="Comma-separated list of topics")
    success_metrics = models.TextField(blank=True, help_text="Metrics set by SWE for each round")
    time_limit = models.PositiveIntegerField(default=3, help_text="Time limit in minutes")
    # score_threshold = models.PositiveIntegerField(default=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['round_number']
        verbose_name = "Round"
        verbose_name_plural = "Rounds"
        unique_together = ('role', 'round_number')

    def __str__(self):
        return f"{self.role.title} - Round {self.round_number}: {self.name}"

    @property
    def data_structures_list(self):
        """Returns data_structures as a list"""
        return [s.strip() for s in self.data_structures.split(',') if s.strip()]

    @property
    def success_metrics_list(self):
        return [s.strip() for s in self.success_metrics.split(',') if s.strip()]

class Question(models.Model):
    """Represents a coding question for an interview round"""
    title = models.CharField(max_length=300, unique=True, help_text="LeetCode title to avoid repeats")
    statement = models.TextField(help_text="The problem statement/description")
    test_cases = models.JSONField(help_text="Test cases as JSON dict")
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return f"{self.title} (Round: {self.round})"


class Interview(models.Model):
    """Represents an interview session between a candidate and interviewer for a specific round"""
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='interviews')
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='interviews')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True, related_name='interviews', help_text="The specific question asked in this interview")
    score = models.PositiveIntegerField(
        default=0, # set min max to 0 100 for interview score
        help_text="Interview score as percentage (0-100)"
    )
    notes = models.TextField(blank=True, help_text="Interview notes and feedback")
    screen_video = models.URLField(max_length=500, blank=True, help_text="URL to screen recording video")
    candidate_video = models.URLField(max_length=500, blank=True, help_text="URL to candidate video recording")
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Interview"
        verbose_name_plural = "Interviews"

    def __str__(self):
        return f"{self.candidate} - {self.round.role.title} Round {self.round.round_number}"
