import datetime

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from django_scopes import scope
from django_scopes.state import scopes_disabled

from ..models import ChickenGroup, Egg
from ..utils import today_midnight

User = get_user_model()


class EggsListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("hop", password="hop")
        with scope(tenant=self.user.tenant_id):
            self.group = ChickenGroup.objects.create(name="Group hop")

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
        response = self.client.get(reverse("eggs_list", kwargs={"minus_days": 10}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(10, response.context["minus_days"])

    def test_eggs_list_with_egg_entries(self):
        """
        Make some entries and show them.
        """
        self.client.force_login(self.user)
        with scope(tenant=self.user.tenant_id):
            Egg.objects.create()
            Egg.objects.create(laid=today_midnight() - datetime.timedelta(days=1))
            Egg.objects.create(laid=today_midnight() - datetime.timedelta(days=1))
            Egg.objects.create(laid=today_midnight() - datetime.timedelta(days=1))

            Egg.objects.create(laid=today_midnight() - datetime.timedelta(days=11))

            response = self.client.get(reverse("eggs_list", kwargs={"minus_days": 10}))
            self.assertEqual(response.status_code, 200)

            # todays entries and after 10 days are not counted
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

            post = {"year": date.year, "month": date.month, "day": date.day}
            url = reverse("eggs_delete", kwargs=post)
            response = self.client.post(url, post)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse("eggs_list"))
            self.assertEqual(Egg.objects.count(), 1)
            user_info = [m.message for m in get_messages(response.wsgi_request)]
            self.assertIn("2 Einträge gelöscht.", user_info)

    def test_eggs_delete_get(self):
        date = datetime.datetime(
            year=2020, month=1, day=1, tzinfo=timezone.get_current_timezone()
        )
        self.client.force_login(self.user)
        with scope(tenant=self.user.tenant_id):
            egg = Egg.objects.create(laid=date)

            self.assertEqual(Egg.objects.count(), 1)

            post = {"year": date.year, "month": date.month, "day": date.day}
            url = reverse("eggs_delete", kwargs=post)
            response = self.client.get(url, post)
            self.assertIn(egg, response.context["eggs"])

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
            }
            url = reverse("eggs_delete", kwargs=post)
            response = self.client.post(url, post)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse("eggs_list"))
            self.assertEqual(Egg.objects.count(), 1)
            user_info = [m.message for m in get_messages(response.wsgi_request)]
            self.assertEqual(len(user_info), 1)

    def test_eggs_insert_entry(self):
        self.client.force_login(self.user)
        with scope(tenant=self.user.tenant_id):
            post = {
                "laid": "2020-01-01",
                "quantity": 5,
                "group": self.group.id,
                "error": Egg.Error.NONE,
                "size": Egg.Size.NONE,
            }
            url = reverse("eggs_list", kwargs={"minus_days": 10})
            response = self.client.post(url, post)

            self.assertEqual(response.status_code, 302)
            print(response)
            self.assertEqual(
                response.url, reverse("eggs_list", kwargs={"minus_days": 10})
            )
            self.assertEqual(Egg.objects.count(), 1)
            self.assertEqual(Egg.objects.first().quantity, 5)

            user_info = [m.message for m in get_messages(response.wsgi_request)]
            # self.assertIn("2 Einträge gelöscht.", user_info)

    def test_eggs_insert_entry_double(self):
        self.client.force_login(self.user)
        with scope(tenant=self.user.tenant_id):
            post = {
                "laid": "2020-01-01",
                "quantity": 5,
                "group": self.group.id,
                "error": Egg.Error.NONE,
                "size": Egg.Size.NONE,
            }
            url = reverse("eggs_list", kwargs={"minus_days": 10})
            response = self.client.post(url, post)
            response_second = self.client.post(url, post)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response_second.status_code, 302)

            self.assertEqual(Egg.objects.count(), 2)
            self.assertEqual(Egg.objects.first().quantity, 5)

    def test_eggs_stats(self):
        self.client.force_login(self.user)
        with scope(tenant=self.user.tenant_id):
            Egg.objects.create(laid=today_midnight() - datetime.timedelta(days=1))
            Egg.objects.create(
                laid=today_midnight() - datetime.timedelta(days=2),
                group_id=self.group.id,
            )
            Egg.objects.create(laid=today_midnight() - datetime.timedelta(days=4))

        self.client.force_login(self.user)
        response = self.client.get(
            reverse("eggs_list_stats", kwargs={"minus_days": 10})
        )
        self.assertEqual(response.status_code, 200)
