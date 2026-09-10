from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Resume
from .views import get_resume_pdf_template_name


class ResumeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="strongpass123",
            first_name="Test",
            last_name="2000-01-01",
        )
        self.client.force_login(self.user)
        session = self.client.session
        session["name"] = "Test"
        session["dob"] = "2000-01-01"
        session.save()

        self.resume = Resume.objects.create(
            name="Test",
            dob=date(2000, 1, 1),
            email="test@example.com",
            phone="1234567890",
            address="Dhaka",
            professional_summary="Experienced developer.",
            company="Example Co",
            job_title="Developer",
            duration="2 years",
            experience_describtion="Built products.",
            college="BUET",
            degree="BSc",
            passing_year="2022",
            skill1="Python",
            skill2="Django",
            skill3="JavaScript",
            skill4="CSS",
            project_name="Portfolio",
            project_description="Created a portfolio project.",
            template="1",
        )

    def test_show_page_lists_user_resumes(self):
        response = self.client.get("/show/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Resume 1")
        self.assertContains(response, "Download PDF")
        self.assertContains(response, self.resume.email)

    def test_download_pdf_returns_pdf_response(self):
        response = self.client.get(f"/download-pdf/{self.resume.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn("attachment; filename=resume-", response["Content-Disposition"])

    def test_resume_pdf_template_name_matches_saved_template(self):
        self.assertEqual(get_resume_pdf_template_name(self.resume), "resume1.html")
