from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSmokeTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create(
            username="test_admin",
            password="super-secure",
            is_staff=True,
            is_superuser=True,
        )
        return super().setUpTestData()

    def test_load_admin_pages(self):
        """Load each admin change and add page to check syntax in the admin classes."""
        self.client.force_login(self.user)

        views = [
            "admin:wordtracker_project_add",
            "admin:wordtracker_project_changelist",
            "admin:wordtracker_worksession_add",
            "admin:wordtracker_worksession_changelist",
        ]

        for view in views:
            with self.subTest(view=view):
                resp = self.client.get(reverse(view))
                self.assertEqual(resp.status_code, 200)
