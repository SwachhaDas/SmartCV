from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile, Education, Experience, Skill, Project, SocialLink


# ==================== MODEL TESTS ====================

class ProfileModelTest(TestCase):
    """Test Profile model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_profile_created_automatically(self):
        """Profile should be auto-created when user is created."""
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_profile_str(self):
        """Profile __str__ should return username's profile."""
        profile = self.user.profile
        self.assertEqual(str(profile), "testuser's profile")

    def test_default_values(self):
        """Profile should have default values."""
        profile = self.user.profile
        self.assertTrue(profile.is_public)
        self.assertEqual(profile.visitor_count, 0)
        self.assertEqual(profile.template, 'classic')


class EducationModelTest(TestCase):
    """Test Education model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.edu = Education.objects.create(
            user=self.user,
            institute='ABC University',
            degree='BSc in CSE',
            cgpa=3.75,
            passing_year=2025,
        )

    def test_education_creation(self):
        self.assertEqual(self.edu.institute, 'ABC University')
        self.assertEqual(self.edu.degree, 'BSc in CSE')

    def test_education_str(self):
        expected = "BSc in CSE - ABC University"
        self.assertEqual(str(self.edu), expected)

    def test_ordering(self):
        """Educations should be ordered by -passing_year."""
        edu2 = Education.objects.create(
            user=self.user, institute='XYZ', degree='MSc', passing_year=2027
        )
        educations = list(Education.objects.all())
        self.assertEqual(educations[0], edu2)  # Latest first


class ExperienceModelTest(TestCase):
    """Test Experience model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_experience_creation(self):
        from datetime import date
        exp = Experience.objects.create(
            user=self.user,
            company='XYZ Corp',
            designation='Developer',
            start_date=date(2024, 1, 1),
        )
        self.assertEqual(exp.company, 'XYZ Corp')
        self.assertIsNone(exp.end_date)


class SkillModelTest(TestCase):
    """Test Skill model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_skill_creation(self):
        skill = Skill.objects.create(
            user=self.user, skill_name='Python', level='expert'
        )
        self.assertEqual(skill.skill_name, 'Python')
        self.assertEqual(skill.level, 'expert')

    def test_default_level(self):
        skill = Skill.objects.create(user=self.user, skill_name='Java')
        self.assertEqual(skill.level, 'beginner')


# ==================== VIEW TESTS ====================

class AuthViewTest(TestCase):
    """Test authentication views."""

    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after register
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='newuser').exists())

    def test_dashboard_requires_login(self):
        """Dashboard should redirect to login if not authenticated."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class CRUDViewTest(TestCase):
    """Test CRUD views."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_education_list(self):
        response = self.client.get(reverse('education_list'))
        self.assertEqual(response.status_code, 200)

    def test_education_add(self):
        from datetime import date
        response = self.client.post(reverse('education_add'), {
            'institute': 'ABC University',
            'degree': 'BSc CSE',
            'cgpa': 3.75,
            'passing_year': 2025,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Education.objects.count(), 1)

    def test_education_edit(self):
        edu = Education.objects.create(
            user=self.user, institute='ABC', degree='BSc', passing_year=2025
        )
        response = self.client.post(reverse('education_edit', args=[edu.pk]), {
            'institute': 'XYZ University',
            'degree': 'BSc CSE',
            'cgpa': 3.80,
            'passing_year': 2025,
        })
        edu.refresh_from_db()
        self.assertEqual(edu.institute, 'XYZ University')

    def test_education_delete(self):
        edu = Education.objects.create(
            user=self.user, institute='ABC', degree='BSc', passing_year=2025
        )
        response = self.client.post(reverse('education_delete', args=[edu.pk]))
        self.assertEqual(Education.objects.count(), 0)

    def test_user_cannot_edit_others_data(self):
        """User should not be able to edit other users' data."""
        other_user = User.objects.create_user(username='other', password='pass123')
        other_edu = Education.objects.create(
            user=other_user, institute='Other', degree='BSc', passing_year=2025
        )
        response = self.client.get(reverse('education_edit', args=[other_edu.pk]))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_skill_add(self):
        response = self.client.post(reverse('skill_add'), {
            'skill_name': 'Python', 'level': 'expert'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Skill.objects.count(), 1)

    def test_project_add(self):
        response = self.client.post(reverse('project_add'), {
            'project_name': 'Test Project',
            'description': 'A test project',
            'live_link': 'https://example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), 1)

    def test_sociallink_add(self):
        response = self.client.post(reverse('sociallink_add'), {
            'platform': 'GitHub',
            'url': 'https://github.com/testuser',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SocialLink.objects.count(), 1)


class PublicPortfolioTest(TestCase):
    """Test public portfolio view."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_public_portfolio(self):
        response = self.client.get(reverse('public_portfolio', args=['testuser']))
        self.assertEqual(response.status_code, 200)

    def test_visitor_counter_increments(self):
        profile = self.user.profile
        initial_count = profile.visitor_count
        self.client.get(reverse('public_portfolio', args=['testuser']))
        profile.refresh_from_db()
        self.assertEqual(profile.visitor_count, initial_count + 1)

    def test_private_portfolio(self):
        profile = self.user.profile
        profile.is_public = False
        profile.save()
        response = self.client.get(reverse('public_portfolio', args=['testuser']))
        self.assertContains(response, 'Private')

    def test_nonexistent_user_redirects(self):
        response = self.client.get(reverse('public_portfolio', args=['nouser']))
        self.assertEqual(response.status_code, 302)


class PDFDownloadTest(TestCase):
    """Test PDF download view."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_pdf_download_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('download_pdf'))
        self.assertEqual(response.status_code, 302)

    def test_pdf_download(self):
        response = self.client.get(reverse('download_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('testuser_resume.pdf', response['Content-Disposition'])