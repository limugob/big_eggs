from django.test import SimpleTestCase
from django.urls import reverse


class MainViewsTests(SimpleTestCase):
    databases = "__all__"

    def test_impressum(self):
        response = self.client.get(reverse("impressum"))
        self.assertContains(response, "Bogumil Schube")

    def test_datenschutz(self):
        response = self.client.get(reverse("datenschutz"))
        self.assertContains(response, "Bogumil Schube")
