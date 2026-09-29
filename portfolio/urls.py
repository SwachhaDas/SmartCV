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
    # Home
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Profile & Dashboard
    path('profile/', views.profile_update, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Education
    path('education/', EducationListView.as_view(), name='education_list'),
    path('education/add/', EducationCreateView.as_view(), name='education_add'),
    path('education/<int:pk>/edit/', EducationUpdateView.as_view(), name='education_edit'),
    path('education/<int:pk>/delete/', EducationDeleteView.as_view(), name='education_delete'),

    # Experience
    path('experience/', ExperienceListView.as_view(), name='experience_list'),
    path('experience/add/', ExperienceCreateView.as_view(), name='experience_add'),
    path('experience/<int:pk>/edit/', ExperienceUpdateView.as_view(), name='experience_edit'),
    path('experience/<int:pk>/delete/', ExperienceDeleteView.as_view(), name='experience_delete'),

    # Skill
    path('skill/', SkillListView.as_view(), name='skill_list'),
    path('skill/add/', SkillCreateView.as_view(), name='skill_add'),
    path('skill/<int:pk>/edit/', SkillUpdateView.as_view(), name='skill_edit'),
    path('skill/<int:pk>/delete/', SkillDeleteView.as_view(), name='skill_delete'),

    # Project
    path('project/', ProjectListView.as_view(), name='project_list'),
    path('project/add/', ProjectCreateView.as_view(), name='project_add'),
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),

    # Social Link
    path('social/', SocialLinkListView.as_view(), name='sociallink_list'),
    path('social/add/', SocialLinkCreateView.as_view(), name='sociallink_add'),
    path('social/<int:pk>/edit/', SocialLinkUpdateView.as_view(), name='sociallink_edit'),
    path('social/<int:pk>/delete/', SocialLinkDeleteView.as_view(), name='sociallink_delete'),

    # Public Portfolio
    path('u/<str:username>/', views.public_portfolio, name='public_portfolio'),
]