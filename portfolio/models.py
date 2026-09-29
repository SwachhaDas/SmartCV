from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """User profile with extra info and portfolio settings."""

    TEMPLATE_CHOICES = [
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('minimal', 'Minimal'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='classic')
    is_public = models.BooleanField(default=True)
    visitor_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Education(models.Model):
    """User's educational background."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    institute = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    passing_year = models.PositiveIntegerField()

    class Meta:
        ordering = ['-passing_year']

    def __str__(self):
        return f"{self.degree} - {self.institute}"


class Experience(models.Model):
    """User's work experience."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.designation} at {self.company}"


class Skill(models.Model):
    """User's skills with proficiency level."""

    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')

    class Meta:
        ordering = ['skill_name']

    def __str__(self):
        return self.skill_name


class Project(models.Model):
    """User's portfolio projects."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=200)
    description = models.TextField()
    live_link = models.URLField(blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.project_name


class SocialLink(models.Model):
    """User's social media links."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=50)
    url = models.URLField()

    class Meta:
        ordering = ['platform']

    def __str__(self):
        return f"{self.platform} - {self.user.username}"