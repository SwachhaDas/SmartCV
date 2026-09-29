from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Education, Experience, Skill, Project, SocialLink


# ============ AUTHENTICATION FORMS ============

class UserRegisterForm(UserCreationForm):
    """Form for new user registration with email field."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """Form to update Django User fields (username, email)."""

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    """Form to update user's Profile info."""

    class Meta:
        model = Profile
        fields = ['bio', 'phone', 'photo', 'template', 'is_public']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'template': forms.Select(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ============ CRUD FORMS ============

class EducationForm(forms.ModelForm):
    """Form for Education CRUD."""

    class Meta:
        model = Education
        fields = ['institute', 'degree', 'cgpa', 'passing_year']
        widgets = {
            'institute': forms.TextInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'passing_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ExperienceForm(forms.ModelForm):
    """Form for Experience CRUD with date validation."""

    class Meta:
        model = Experience
        fields = ['company', 'designation', 'start_date', 'end_date', 'description']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        """Validate that end_date is after start_date."""
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start and end and end < start:
            raise forms.ValidationError("End date must be after start date.")
        return cleaned_data


class SkillForm(forms.ModelForm):
    """Form for Skill CRUD."""

    class Meta:
        model = Skill
        fields = ['skill_name', 'level']
        widgets = {
            'skill_name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
        }


class ProjectForm(forms.ModelForm):
    """Form for Project CRUD."""

    class Meta:
        model = Project
        fields = ['project_name', 'description', 'live_link']
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'live_link': forms.URLInput(attrs={'class': 'form-control'}),
        }


class SocialLinkForm(forms.ModelForm):
    """Form for SocialLink CRUD."""

    class Meta:
        model = SocialLink
        fields = ['platform', 'url']
        widgets = {
            'platform': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }