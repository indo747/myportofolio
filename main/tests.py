import datetime
import json

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


class ExperienceCrudTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
        )
        self.valid_data = {
            "title": "Student Assistant",
            "description": "Ran tutorial groups.",
            "category": "part-time",
            "thumbnail": "",
            "ended_at": "",
        }

    def test_create_form_is_accessible(self):
        response = self.client.get(reverse("main:create_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_create_experience(self):
        response = self.client.post(reverse("main:create_experience"), self.valid_data)
        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(Experience.objects.filter(title="Student Assistant").exists())

    def test_create_rejects_missing_title(self):
        response = self.client.post(reverse("main:create_experience"), {**self.valid_data, "title": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form-error")
        self.assertEqual(Experience.objects.count(), 1)

    def test_update_form_is_prefilled(self):
        response = self.client.get(reverse("main:update_experience", args=[self.experience.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'value="{self.experience.title}"')

    def test_update_experience(self):
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {**self.valid_data, "title": "Head Teaching Assistant", "ended_at": "2025-06-30T12:00"},
        )
        self.assertRedirects(response, reverse("main:show_experience"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Head Teaching Assistant")
        self.assertFalse(self.experience.is_ongoing)

    def test_delete_needs_post(self):
        url = reverse("main:delete_experience", args=[self.experience.id])
        self.client.get(url)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())
        self.client.post(url)
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_experience_json(self):
        response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["title"], self.experience.title)

    def test_experience_json_filters_by_title(self):
        Experience.objects.create(title="Working Student", description="x", category="research")
        response = self.client.get(reverse("main:get_experience_json"), {"title": "teaching"})
        titles = [entry["fields"]["title"] for entry in json.loads(response.content)]
        self.assertEqual(titles, [self.experience.title])

    def test_search_without_result_says_so(self):
        response = self.client.get(reverse("main:show_experience"), {"title": "nothing here"})
        self.assertContains(response, "No experience matches that search.")
        self.assertNotContains(response, self.experience.title)


class EducationUpdateTest(TestCase):
    def setUp(self):
        self.education = Education.objects.create(
            degree="MSc Computer Science",
            institution="TU Darmstadt",
            level="master",
            started_at=datetime.date(2026, 4, 1),
        )

    def test_update_form_is_prefilled(self):
        response = self.client.get(reverse("main:update_education", args=[self.education.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education_form.html")
        self.assertContains(response, 'value="MSc Computer Science"')
        self.assertContains(response, "Edit Education")

    def test_update_education(self):
        response = self.client.post(
            reverse("main:update_education", args=[self.education.id]),
            {
                "degree": "MSc Data Science",
                "institution": "TU Darmstadt",
                "level": "master",
                "description": "",
                "started_at": "2026-04-01",
                "ended_at": "",
            },
        )
        self.assertRedirects(response, reverse("main:show_education"))
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "MSc Data Science")
