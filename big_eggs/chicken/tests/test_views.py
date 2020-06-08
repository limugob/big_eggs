import datetime

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from django_scopes import scope

from ..models import Egg
from ..utils import today_midnight

User = get_user_model()


class EggsListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("hop", password="hop")

    def test_no_login(self):
        """
        If not logged in, redirect.
        """
        response = self.client.get(reverse("eggs_list"), follow=True)
        self.assertIn("login", response.redirect_chain[0][0])
        self.assertEqual(302, response.redirect_chain[0][1])

    def test_eggs_list_no_egg_entries(self):
        """
        If no entries, show blank table.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("eggs_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(10, response.context["minus_days"])

    def test_eggs_list_with_egg_entries(self):
        """
        Make some entries and show them.
        """
        self.client.force_login(self.user)
        with scope(tenant=self.user.tenant_id):
            Egg.objects.create()
            Egg.objects.create()
            Egg.objects.create()

            Egg.objects.create(laid=today_midnight() - datetime.timedelta(days=10))

            response = self.client.get(reverse("eggs_list"))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(3, response.context["sum_all"])
            self.assertEqual(10, response.context["minus_days"])
            self.assertEqual(0.3, response.context["average"])

            response = self.client.get(reverse("eggs_list", kwargs={"minus_days": 20}))
            self.assertEqual(4, response.context["sum_all"])
            self.assertEqual(20, response.context["minus_days"])

    def test_eggs_delete(self):
        date = datetime.datetime(
            year=2020, month=1, day=1, tzinfo=timezone.get_current_timezone()
        )
        self.client.force_login(self.user)
        with scope(tenant=self.user.tenant_id):
            Egg.objects.create(laid=date)
            Egg.objects.create(laid=date)

            # one Egg has different date
            Egg.objects.create(laid=date - datetime.timedelta(days=1))

            self.assertEqual(Egg.objects.count(), 3)

            post = {
                "year": date.year,
                "month": date.month,
                "day": date.day,
                "group": "None",
                "error": "N",
            }
            url = reverse("eggs_delete", kwargs=post)
            response = self.client.post(url, post)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse("eggs_list"))
            self.assertEqual(Egg.objects.count(), 1)
            user_info = [m.message for m in get_messages(response.wsgi_request)]
            self.assertIn("2 Einträge gelöscht.", user_info)

    def test_eggs_delete_no_data(self):
        date = datetime.datetime(
            year=2020, month=1, day=1, tzinfo=timezone.get_current_timezone()
        )
        self.client.force_login(self.user)
        with scope(tenant=self.user.tenant_id):
            Egg.objects.create(laid=date - datetime.timedelta(days=2))
            self.assertEqual(Egg.objects.count(), 1)

            post = {
                "year": date.year,
                "month": date.month,
                "day": date.day,
                "group": "None",
                "error": "N",
            }
            url = reverse("eggs_delete", kwargs=post)
            response = self.client.post(url, post)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse("eggs_list"))
            self.assertEqual(Egg.objects.count(), 1)
            user_info = [m.message for m in get_messages(response.wsgi_request)]
            self.assertEqual(len(user_info), 1)
