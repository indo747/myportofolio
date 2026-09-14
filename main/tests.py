import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Education, Experience


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "PBP Teaching Assistant")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "No experience has been added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))
        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")


class EducationTest(TestCase):
    def setUp(self):
        self.education = Education.objects.create(
            degree="MSc Computer Science",
            institution="TU Darmstadt",
            level="master",
            description="Currently enrolled.",
            started_at=datetime.date(2026, 4, 1),
        )

    def test_education_url_is_accessible(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_education_page_shows_model_data(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, self.education.degree)
        self.assertContains(response, self.education.institution)
        self.assertContains(response, "Master")
        self.assertContains(response, "to present")

    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, "No education has been added yet.")

    def test_finished_education_shows_end_year(self):
        self.education.ended_at = datetime.date(2028, 3, 31)
        self.education.save()
        response = self.client.get(reverse("main:show_education"))
        self.assertFalse(self.education.is_current)
        self.assertContains(response, "to 2028")
        self.assertNotContains(response, "to present")

    def test_education_model(self):
        self.assertEqual(str(self.education), "MSc Computer Science, TU Darmstadt")
        self.assertTrue(self.education.is_current)

    def test_education_is_ordered_by_start_date(self):
        older = Education.objects.create(
            degree="BSc Computer Science",
            institution="Goethe University Frankfurt",
            level="bachelor",
            started_at=datetime.date(2022, 10, 1),
            ended_at=datetime.date(2026, 8, 25),
        )
        self.assertEqual(list(Education.objects.all()), [self.education, older])

    def test_navbar_links_to_education(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertContains(response, f'href="{reverse("main:show_education")}"')
