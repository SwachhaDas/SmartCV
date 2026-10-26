from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponse, JsonResponse, Http404
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.http import require_GET, require_http_methods, require_POST
import json

from .models import Profile, Education, Experience, Skill, Project, SocialLink, ActivityHistory
from .forms import (
    UserRegisterForm, UserUpdateForm, ProfileUpdateForm,
    EducationForm, ExperienceForm, SkillForm, ProjectForm, SocialLinkForm
)
from .pdf_utils import build_cv_pdf
from .template_registry import PORTFOLIO_TEMPLATES, DEFAULT_SLUG, get_template, is_valid_slug


def build_portfolio_context(owner):
    profile = owner.profile
    return {
        "profile_user": owner, "profile": profile,
        "educations": owner.educations.all(), "experiences": owner.experiences.all(),
        "skills": owner.skills.all(), "projects": owner.projects.all(),
        "social_links": owner.social_links.all(), "website_mode": getattr(profile, "is_website_mode", False),
    }


def home(request):
    return render(request, 'portfolio/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'portfolio/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'portfolio/login.html'


class CustomLogoutView(LogoutView):
    next_page = 'home'


@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save(); p_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'portfolio/profile.html', {'u_form': u_form, 'p_form': p_form})


@login_required
def dashboard(request):
    u = request.user
    checks = [
        ("Add your education", u.educations.exists(), "education_add", 25),
        ("Add work experience", u.experiences.exists(), "experience_add", 20),
        ("Add at least 3 skills", u.skills.count() >= 3, "skill_add", 20),
        ("Add a project", u.projects.exists(), "project_add", 20),
        ("Add a social link", u.social_links.exists(), "sociallink_add", 15),
    ]
    percent = sum(weight for _, done, _, weight in checks if done)
    steps = [{"label": l, "done": d, "url_name": u_name} for l, d, u_name, _ in checks]
    completion = {"percent": percent, "steps": steps}
    stat_cards = [
        ("bi-mortarboard-fill", "Education", u.educations.count(), "education_list"),
        ("bi-briefcase-fill", "Experience", u.experiences.count(), "experience_list"),
        ("bi-lightning-charge-fill", "Skills", u.skills.count(), "skill_list"),
        ("bi-kanban-fill", "Projects", u.projects.count(), "project_list"),
    ]
    recent_activity = ActivityHistory.objects.filter(user=u).order_by("-timestamp")[:5]
    context = {'completion': completion, 'stat_cards': stat_cards, 'recent_activity': recent_activity}
    return render(request, 'portfolio/dashboard.html', context)


# ==================== EDUCATION CRUD ====================
class EducationListView(LoginRequiredMixin, ListView):
    model = Education; template_name = 'portfolio/education_list.html'; context_object_name = 'educations'
    def get_queryset(self): return Education.objects.filter(user=self.request.user)

class EducationCreateView(LoginRequiredMixin, CreateView):
    model = Education; form_class = EducationForm; template_name = 'portfolio/education_form.html'; success_url = reverse_lazy('education_list')
    def form_valid(self, form): form.instance.user = self.request.user; messages.success(self.request, "Education added successfully!"); return super().form_valid(form)

class EducationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Education; form_class = EducationForm; template_name = 'portfolio/education_form.html'; success_url = reverse_lazy('education_list')
    def test_func(self): return self.get_object().user == self.request.user

class EducationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Education; template_name = 'portfolio/confirm_delete.html'; success_url = reverse_lazy('education_list')
    def test_func(self): return self.get_object().user == self.request.user


# ==================== EXPERIENCE CRUD ====================
class ExperienceListView(LoginRequiredMixin, ListView):
    model = Experience; template_name = 'portfolio/experience_list.html'; context_object_name = 'experiences'
    def get_queryset(self): return Experience.objects.filter(user=self.request.user)

class ExperienceCreateView(LoginRequiredMixin, CreateView):
    model = Experience; form_class = ExperienceForm; template_name = 'portfolio/experience_form.html'; success_url = reverse_lazy('experience_list')
    def form_valid(self, form): form.instance.user = self.request.user; messages.success(self.request, "Experience added successfully!"); return super().form_valid(form)

class ExperienceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Experience; form_class = ExperienceForm; template_name = 'portfolio/experience_form.html'; success_url = reverse_lazy('experience_list')
    def test_func(self): return self.get_object().user == self.request.user

class ExperienceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Experience; template_name = 'portfolio/confirm_delete.html'; success_url = reverse_lazy('experience_list')
    def test_func(self): return self.get_object().user == self.request.user


# ==================== SKILL CRUD ====================
class SkillListView(LoginRequiredMixin, ListView):
    model = Skill; template_name = 'portfolio/skill_list.html'; context_object_name = 'skills'
    def get_queryset(self): return Skill.objects.filter(user=self.request.user)

class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill; form_class = SkillForm; template_name = 'portfolio/skill_form.html'; success_url = reverse_lazy('skill_list')
    def form_valid(self, form): form.instance.user = self.request.user; messages.success(self.request, "Skill added successfully!"); return super().form_valid(form)

class SkillUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Skill; form_class = SkillForm; template_name = 'portfolio/skill_form.html'; success_url = reverse_lazy('skill_list')
    def test_func(self): return self.get_object().user == self.request.user

class SkillDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Skill; template_name = 'portfolio/confirm_delete.html'; success_url = reverse_lazy('skill_list')
    def test_func(self): return self.get_object().user == self.request.user


# ==================== PROJECT CRUD ====================
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project; template_name = 'portfolio/project_list.html'; context_object_name = 'projects'
    def get_queryset(self): return Project.objects.filter(user=self.request.user)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project; form_class = ProjectForm; template_name = 'portfolio/project_form.html'; success_url = reverse_lazy('project_list')
    def form_valid(self, form): form.instance.user = self.request.user; messages.success(self.request, "Project added successfully!"); return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project; form_class = ProjectForm; template_name = 'portfolio/project_form.html'; success_url = reverse_lazy('project_list')
    def test_func(self): return self.get_object().user == self.request.user

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project; template_name = 'portfolio/confirm_delete.html'; success_url = reverse_lazy('project_list')
    def test_func(self): return self.get_object().user == self.request.user


# ==================== SOCIAL LINK CRUD ====================
class SocialLinkListView(LoginRequiredMixin, ListView):
    model = SocialLink; template_name = 'portfolio/sociallink_list.html'; context_object_name = 'social_links'
    def get_queryset(self): return SocialLink.objects.filter(user=self.request.user)

class SocialLinkCreateView(LoginRequiredMixin, CreateView):
    model = SocialLink; form_class = SocialLinkForm; template_name = 'portfolio/sociallink_form.html'; success_url = reverse_lazy('sociallink_list')
    def form_valid(self, form): form.instance.user = self.request.user; messages.success(self.request, "Social link added successfully!"); return super().form_valid(form)

class SocialLinkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SocialLink; form_class = SocialLinkForm; template_name = 'portfolio/sociallink_form.html'; success_url = reverse_lazy('sociallink_list')
    def test_func(self): return self.get_object().user == self.request.user

class SocialLinkDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SocialLink; template_name = 'portfolio/confirm_delete.html'; success_url = reverse_lazy('sociallink_list')
    def test_func(self): return self.get_object().user == self.request.user


# ==================== PORTFOLIO & TEMPLATE STUDIO ====================

@login_required
@require_http_methods(["GET", "POST"])
def template_selector(request):
    profile = request.user.profile
    if request.method == "POST":
        slug = request.POST.get("template", "")
        wants_json = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        if not is_valid_slug(slug):
            if wants_json: return JsonResponse({"ok": False, "error": "Unknown template."}, status=400)
        else:
            profile.template = slug
            profile.is_website_mode = False
            profile.save(update_fields=["template", "is_website_mode"])
            if wants_json: return JsonResponse({"ok": True, "slug": slug, "name": get_template(slug)["name"]})
    current = profile.template if is_valid_slug(getattr(profile, "template", "")) else DEFAULT_SLUG
    return render(request, "portfolio/template_select.html", {"portfolio_templates": PORTFOLIO_TEMPLATES, "current_template": current})


_PREVIEW_HELPERS = """
<base target="_blank">
<script>
  document.addEventListener('click', function (e) { var a = e.target.closest && e.target.closest('a'); if (a) { e.preventDefault(); } }, true);
  document.addEventListener('submit', function (e) { e.preventDefault(); }, true);
</script>
"""

@login_required
@require_GET
@never_cache
def template_preview(request, slug):
    if not is_valid_slug(slug): raise Http404("Unknown template")
    tpl = get_template(slug)
    html = render_to_string(tpl["html"], build_portfolio_context(request.user), request=request)
    if "</head>" in html: html = html.replace("</head>", _PREVIEW_HELPERS + "</head>", 1)
    else: html = _PREVIEW_HELPERS + html
    return HttpResponse(html)

def public_portfolio(request, username):
    try:
        user = User.objects.get(username=username); profile = user.profile
    except (User.DoesNotExist, Profile.DoesNotExist):
        messages.error(request, "User not found."); return redirect('home')
    if not profile.is_public: return render(request, 'portfolio/private.html')
    profile.visitor_count += 1; profile.save()
    context = build_portfolio_context(user)
    if profile.is_website_mode: return render(request, 'portfolio/website_mode.html', context)
    slug = getattr(profile, "template", DEFAULT_SLUG)
    tpl = get_template(slug)
    return render(request, tpl["html"], context)


# ==================== PDF STUDIO & DOWNLOAD ====================

@login_required
def pdf_template_select_view(request):
    """The PDF Studio page itself."""
    profile = request.user.profile
    return render(request, "portfolio/pdf_template_select.html", {
        "current_template": profile.pdf_template or "classic",
        "current_type": request.GET.get("type", "academic"),
    })

@login_required
@never_cache
@xframe_options_sameorigin  # <-- Fixes "refused to connect" iframe issue
def pdf_download_view(request, type="academic", template="classic"):
    """Unified view for preview and download."""
    VALID_TYPES = {"academic", "job", "faculty"}
    VALID_TEMPLATES = {"classic", "modern", "minimal"}
    
    if type not in VALID_TYPES or template not in VALID_TEMPLATES:
        raise Http404("Unknown CV type or template")

    pdf_buffer = build_cv_pdf(request.user, cv_type=type, template_slug=template)
    pdf_bytes = pdf_buffer.getvalue() if hasattr(pdf_buffer, "getvalue") else pdf_buffer

    # ?download=1 for attachment (download), otherwise inline (for iframe preview)
    disposition = "attachment" if request.GET.get("download") else "inline"
    filename = f"{request.user.username}_{type}_{template}_cv.pdf"

    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'{disposition}; filename="{filename}"'
    response["Content-Length"] = len(pdf_bytes)
    return response


@login_required
def download_resume_pdf(request):
    """Fallback download endpoint."""
    user = request.user
    cv_type = request.GET.get('type', 'job')
    pdf_buffer = build_cv_pdf(user, cv_type=cv_type)
    filename = f"{user.username}_{cv_type}_resume.pdf"
    return FileResponse(pdf_buffer, as_attachment=True, filename=filename, content_type='application/pdf')


# ==================== APPLY TEMPLATE (AJAX) ====================

@login_required
@require_POST
def apply_template(request):
    data = json.loads(request.body or "{}")
    kind, tpl = data.get("kind", "pdf"), data.get("template")
    profile = request.user.profile
    
    if kind == "pdf" and tpl in ["classic", "modern", "minimal"]:
        profile.pdf_template = tpl
        profile.save(update_fields=["pdf_template"])
    elif kind == "html" and tpl in [t[0] for t in Profile.TEMPLATE_CHOICES]:
        profile.template = tpl
        profile.save(update_fields=["template"])
    else:
        return JsonResponse({"ok": False, "error": "Invalid template"}, status=400)
        
    return JsonResponse({
        "ok": True,
        "live_url": reverse("public_portfolio", args=[request.user.username]),
        "pdf_url": reverse("pdf_download", args=["job", tpl]), # job is default, but URL requires type & template
    })


# ==================== GUIDELINE & CV OPTIONS ====================

def guideline(request):
    return render(request, 'portfolio/guideline.html')

def cv_generation_options(request):
    if request.method == 'POST':
        cv_type = request.POST.get('cv_type')
        user = request.user
        # Optional: Validation logic here
        ActivityHistory.objects.create(user=user, action='download_pdf', details=f'Generated {cv_type.capitalize()} CV')
        return redirect('pdf_template_select') # Redirect to PDF Studio instead of downloading directly
    return render(request, 'portfolio/cv_options.html')

@login_required
def activity_history(request):
    activities = ActivityHistory.objects.filter(user=request.user)
    return render(request, 'portfolio/history.html', {'activities': activities})