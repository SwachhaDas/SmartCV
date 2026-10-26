from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # HTML Portfolio Template Choices
    TEMPLATE_CHOICES = [
        ('classic', '1. Classic Corporate'),
        ('modern', '2. Modern Executive'),
        ('minimal', '3. Minimalist Clean'),
        ('dark', '4. Dark Mode Pro'),
        ('timeline', '5. Timeline Professional'),
        ('colorful', '6. Colorful Gradient'),
        ('card', '7. Card Layout'),
        ('sidebar', '8. Sidebar Style'),
        ('academic', '9. Academic CV'),
        ('elegant', '10. Elegant Serif'),
    ]

    # PDF Template Choices (ATS Friendly)
    PDF_TEMPLATE_CHOICES = [
        ('classic', 'Classic (Single Column, ATS)'),
        ('modern', 'Modern (Two-Column Sidebar)'),
        ('minimal', 'Minimal (Elegant Serif)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    
    # HTML Template field
    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='classic')
    
    # PDF Template field (NEW)
    pdf_template = models.CharField(max_length=20, choices=PDF_TEMPLATE_CHOICES, default='classic')
    
    is_public = models.BooleanField(default=True)
    visitor_count = models.PositiveIntegerField(default=0)
    is_website_mode = models.BooleanField(default=False, help_text="Check this to make it a full website.")

    def __str__(self):
        return f"{self.user.username}'s profile"


class ActivityHistory(models.Model):
    """Track user activities (like downloading CV or adding data)."""
    ACTION_CHOICES = [
        ('login', 'Logged In'),
        ('download_pdf', 'Downloaded PDF Resume'),
        ('add_edu', 'Added Education'),
        ('add_exp', 'Added Experience'),
        ('add_proj', 'Added Project'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Activity Histories"

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class Education(models.Model):
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
    PROJECT_TYPES = [
        ('academic', 'Academic Project'),
        ('research', 'Research Project'),
        ('ongoing', 'Ongoing Research'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=200)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='academic')
    description = models.TextField()
    live_link = models.URLField(blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.project_name


class SocialLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=50)
    url = models.URLField()

    class Meta:
        ordering = ['platform']

    def __str__(self):
        return f"{self.platform} - {self.user.username}"