from django.urls import path
from . import views
from .views import (
    CustomLoginView, CustomLogoutView,
    EducationListView, EducationCreateView, EducationUpdateView, EducationDeleteView,
    ExperienceListView, ExperienceCreateView, ExperienceUpdateView, ExperienceDeleteView,
    SkillListView, SkillCreateView, SkillUpdateView, SkillDeleteView,
    ProjectListView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView,
    SocialLinkListView, SocialLinkCreateView, SocialLinkUpdateView, SocialLinkDeleteView,
)

urlpatterns = [
    # ==================== HOME & AUTH ====================
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # ==================== DASHBOARD & PROFILE ====================
    path('profile/', views.profile_update, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # ==================== EDUCATION ====================
    path('education/', EducationListView.as_view(), name='education_list'),
    path('education/add/', EducationCreateView.as_view(), name='education_add'),
    path('education/<int:pk>/edit/', EducationUpdateView.as_view(), name='education_edit'),
    path('education/<int:pk>/delete/', EducationDeleteView.as_view(), name='education_delete'),

    # ==================== EXPERIENCE ====================
    path('experience/', ExperienceListView.as_view(), name='experience_list'),
    path('experience/add/', ExperienceCreateView.as_view(), name='experience_add'),
    path('experience/<int:pk>/edit/', ExperienceUpdateView.as_view(), name='experience_edit'),
    path('experience/<int:pk>/delete/', ExperienceDeleteView.as_view(), name='experience_delete'),

    # ==================== SKILL ====================
    path('skill/', SkillListView.as_view(), name='skill_list'),
    path('skill/add/', SkillCreateView.as_view(), name='skill_add'),
    path('skill/<int:pk>/edit/', SkillUpdateView.as_view(), name='skill_edit'),
    path('skill/<int:pk>/delete/', SkillDeleteView.as_view(), name='skill_delete'),

    # ==================== PROJECT ====================
    path('project/', ProjectListView.as_view(), name='project_list'),
    path('project/add/', ProjectCreateView.as_view(), name='project_add'),
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),

    # ==================== SOCIAL LINK ====================
    path('social/', SocialLinkListView.as_view(), name='sociallink_list'),
    path('social/add/', SocialLinkCreateView.as_view(), name='sociallink_add'),
    path('social/<int:pk>/edit/', SocialLinkUpdateView.as_view(), name='sociallink_edit'),
    path('social/<int:pk>/delete/', SocialLinkDeleteView.as_view(), name='sociallink_delete'),

    # ==================== PORTFOLIO & TEMPLATES ====================
    path('u/<str:username>/', views.public_portfolio, name='public_portfolio'),
    path('templates/', views.template_selector, name='template_selector'),
    path('templates/preview/<slug:slug>/', views.template_preview, name='template_preview'),

    # ==================== CV GENERATION & PDF ====================
    path('guideline/', views.guideline, name='guideline'),
    path('generate-cv/', views.cv_generation_options, name='generate_cv'),
    
    # PDF Studio & Actions
    path('pdf-studio/', views.pdf_template_select_view, name='pdf_template_select'),
    
    # PDF Download for PDF Studio (Accepts type and template in URL)
    path('pdf/<str:type>/<str:template>/', views.pdf_download_view, name='pdf_download'),
    
    # Fallback Download URL (For Claude's HTML templates)
    path('download-pdf/', views.pdf_download_view, {'type': 'job', 'template': 'classic'}, name='download_pdf'),
    
    # Apply Template (AJAX)
    path('studio/apply/', views.apply_template, name='apply_template'),

    # ==================== HISTORY ====================
    path('history/', views.activity_history, name='history'),
]