from django.contrib import admin
from .models import Profile, Education, Experience, Skill, Project, SocialLink


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profile model."""

    list_display = ('user', 'phone', 'template', 'is_public', 'visitor_count')
    list_filter = ('template', 'is_public')
    search_fields = ('user__username', 'user__email')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    """Admin configuration for Education model."""

    list_display = ('user', 'institute', 'degree', 'passing_year')
    list_filter = ('passing_year',)
    search_fields = ('user__username', 'institute', 'degree')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """Admin configuration for Experience model."""

    list_display = ('user', 'company', 'designation', 'start_date')
    search_fields = ('user__username', 'company', 'designation')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin configuration for Skill model."""

    list_display = ('user', 'skill_name', 'level')
    list_filter = ('level',)
    search_fields = ('user__username', 'skill_name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin configuration for Project model."""

    list_display = ('user', 'project_name', 'live_link')
    search_fields = ('user__username', 'project_name')


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    """Admin configuration for SocialLink model."""

    list_display = ('user', 'platform', 'url')
    search_fields = ('user__username', 'platform')