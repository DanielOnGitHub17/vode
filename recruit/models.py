from django.db import models


class Role(models.Model):
    """Represents a job role with multiple interview rounds"""
    title = models.CharField(max_length=200, help_text="Job title (e.g., Backend Engineer)")
    description = models.TextField(blank=True, help_text="Role description and responsibilities")
    num_rounds = models.PositiveIntegerField(
        default=3,
        help_text="Number of interview rounds for this role"
    )
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
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='rounds')
    round_number = models.PositiveIntegerField(help_text="Round number (1, 2, 3, etc.)")
    name = models.CharField(max_length=200, help_text="Round name (e.g., Coding Challenge)")
    description = models.TextField(blank=True, help_text="Description of the round")
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    data_structures = models.TextField(blank=True, help_text="Comma-separated list of topics")
    time_limit = models.PositiveIntegerField(default=30, help_text="Time limit in minutes")
    max_score = models.PositiveIntegerField(default=100, help_text="Maximum score for this round")

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


class Candidate(models.Model):
    """Represents a candidate applying for a role"""
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='candidates')
    current_round = models.PositiveIntegerField(default=1, help_text="Current round number")
    ai_score = models.FloatField(default=0.0, help_text="AI evaluation score (0-1)")
    notes = models.TextField(blank=True)
    needs_review = models.BooleanField(default=False, help_text="Requires manual SWE review")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"

    def __str__(self):
        return f"{self.name} - {self.role.title} (Round {self.current_round})"
