from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import FileResponse
from .models import Profile, Education, Experience, Skill, Project, SocialLink
from .forms import (
    UserRegisterForm, UserUpdateForm, ProfileUpdateForm,
    EducationForm, ExperienceForm, SkillForm, ProjectForm, SocialLinkForm
)
from .pdf_utils import generate_resume_pdf


# ==================== HOME ====================

def home(request):
    """Landing page for SmartCV."""
    return render(request, 'portfolio/home.html')


# ==================== AUTHENTICATION ====================

def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Create profile for new user
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'portfolio/register.html', {'form': form})


class CustomLoginView(LoginView):
    """Custom login view with our template."""
    template_name = 'portfolio/login.html'


class CustomLogoutView(LogoutView):
    """Custom logout redirecting to home."""
    next_page = 'home'


# ==================== PROFILE ====================

@login_required
def profile_update(request):
    """Update user and profile info."""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'portfolio/profile.html', {'u_form': u_form, 'p_form': p_form})


# ==================== DASHBOARD ====================

@login_required
def dashboard(request):
    """User dashboard with counts and quick actions."""
    context = {
        'edu_count': request.user.educations.count(),
        'exp_count': request.user.experiences.count(),
        'skill_count': request.user.skills.count(),
        'proj_count': request.user.projects.count(),
        'social_count': request.user.social_links.count(),
    }
    return render(request, 'portfolio/dashboard.html', context)


# ==================== EDUCATION CRUD ====================

class EducationListView(LoginRequiredMixin, ListView):
    model = Education
    template_name = 'portfolio/education_list.html'
    context_object_name = 'educations'

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)


class EducationCreateView(LoginRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'portfolio/education_form.html'
    success_url = reverse_lazy('education_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Education added successfully!")
        return super().form_valid(form)


class EducationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Education
    form_class = EducationForm
    template_name = 'portfolio/education_form.html'
    success_url = reverse_lazy('education_list')

    def test_func(self):
        return self.get_object().user == self.request.user


class EducationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Education
    template_name = 'portfolio/confirm_delete.html'
    success_url = reverse_lazy('education_list')

    def test_func(self):
        return self.get_object().user == self.request.user


# ==================== EXPERIENCE CRUD ====================

class ExperienceListView(LoginRequiredMixin, ListView):
    model = Experience
    template_name = 'portfolio/experience_list.html'
    context_object_name = 'experiences'

    def get_queryset(self):
        return Experience.objects.filter(user=self.request.user)


class ExperienceCreateView(LoginRequiredMixin, CreateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'portfolio/experience_form.html'
    success_url = reverse_lazy('experience_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Experience added successfully!")
        return super().form_valid(form)


class ExperienceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'portfolio/experience_form.html'
    success_url = reverse_lazy('experience_list')

    def test_func(self):
        return self.get_object().user == self.request.user


class ExperienceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Experience
    template_name = 'portfolio/confirm_delete.html'
    success_url = reverse_lazy('experience_list')

    def test_func(self):
        return self.get_object().user == self.request.user


# ==================== SKILL CRUD ====================

class SkillListView(LoginRequiredMixin, ListView):
    model = Skill
    template_name = 'portfolio/skill_list.html'
    context_object_name = 'skills'

    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user)


class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'portfolio/skill_form.html'
    success_url = reverse_lazy('skill_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Skill added successfully!")
        return super().form_valid(form)


class SkillUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = 'portfolio/skill_form.html'
    success_url = reverse_lazy('skill_list')

    def test_func(self):
        return self.get_object().user == self.request.user


class SkillDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Skill
    template_name = 'portfolio/confirm_delete.html'
    success_url = reverse_lazy('skill_list')

    def test_func(self):
        return self.get_object().user == self.request.user


# ==================== PROJECT CRUD ====================

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Project added successfully!")
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio/project_form.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        return self.get_object().user == self.request.user


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'portfolio/confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        return self.get_object().user == self.request.user


# ==================== SOCIAL LINK CRUD ====================

class SocialLinkListView(LoginRequiredMixin, ListView):
    model = SocialLink
    template_name = 'portfolio/sociallink_list.html'
    context_object_name = 'social_links'

    def get_queryset(self):
        return SocialLink.objects.filter(user=self.request.user)


class SocialLinkCreateView(LoginRequiredMixin, CreateView):
    model = SocialLink
    form_class = SocialLinkForm
    template_name = 'portfolio/sociallink_form.html'
    success_url = reverse_lazy('sociallink_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Social link added successfully!")
        return super().form_valid(form)


class SocialLinkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SocialLink
    form_class = SocialLinkForm
    template_name = 'portfolio/sociallink_form.html'
    success_url = reverse_lazy('sociallink_list')

    def test_func(self):
        return self.get_object().user == self.request.user


class SocialLinkDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SocialLink
    template_name = 'portfolio/confirm_delete.html'
    success_url = reverse_lazy('sociallink_list')

    def test_func(self):
        return self.get_object().user == self.request.user


# ==================== PUBLIC PORTFOLIO ====================

def public_portfolio(request, username):
    """Public portfolio page at /u/<username>/."""
    try:
        user = User.objects.get(username=username)
        profile = user.profile
    except (User.DoesNotExist, Profile.DoesNotExist):
        messages.error(request, "User not found.")
        return redirect('home')

    if not profile.is_public:
        return render(request, 'portfolio/private.html')

    # Increment visitor counter
    profile.visitor_count += 1
    profile.save()

    context = {
        'profile_user': user,
        'profile': profile,
        'educations': user.educations.all(),
        'experiences': user.experiences.all(),
        'skills': user.skills.all(),
        'projects': user.projects.all(),
        'social_links': user.social_links.all(),
    }

    # Choose template based on user's choice
    template_name = f'portfolio/portfolio_{profile.template}.html'
    return render(request, template_name, context)


# ==================== PDF DOWNLOAD ====================

@login_required
def download_resume_pdf(request):
    """Generate and download user's resume as PDF."""
    user = request.user

    # Ensure profile exists
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    # Generate PDF
    pdf_buffer = generate_resume_pdf(
        user=user,
        profile=profile,
        educations=user.educations.all(),
        experiences=user.experiences.all(),
        skills=user.skills.all(),
        projects=user.projects.all(),
        social_links=user.social_links.all(),
    )

    filename = f"{user.username}_resume.pdf"
    return FileResponse(
        pdf_buffer,
        as_attachment=True,
        filename=filename,
        content_type='application/pdf',
    )