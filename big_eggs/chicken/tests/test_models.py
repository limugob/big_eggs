import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from django_scopes import scope

from ..models import Chicken, ChickenGroup, Egg

User = get_user_model()


class ChickenGroupTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("hop", password="hop")
        self.client.force_login(self.user)
        with scope(tenant=self.user.tenant_id):
            cg = ChickenGroup(name="Groupe A")
            # cg.full_clean()   # when is the transaction ?
            cg.save()
            self.cg = cg

    def test_str(self):
        self.assertEqual(str(self.cg), self.cg.name)

    def test_get_absolute_url(self):
        self.assertIsNot(self.cg.get_absolute_url(), "")

    def test_get_members(self):
        with scope(tenant=self.user.tenant_id):
            self.assertEquals(self.cg.get_members().count(), 0)


class ChickenTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("hop", password="hop")
        self.client.force_login(self.user)
        with scope(tenant=self.user.tenant_id):
            c = Chicken(name="Chicken AA")
            c.save()
            self.c = c

    def test_str(self):
        self.assertEquals(str(self.c), self.c.name)

    def test_get_absolute_url(self):
        self.assertIsNot(self.c.get_absolute_url(), "")

    def test_entry_clean(self):
        self.c.clean()

        self.c.entry = self.c.entry - datetime.timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.c.clean()

    def test_departure_clean(self):
        self.c.clean()

        self.c.departure = self.c.entry - datetime.timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.c.clean()

    def test_age(self):
        self.c.age()


class EggTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("hop", password="hop")
        self.client.force_login(self.user)
        with scope(tenant=self.user.tenant_id):
            e = Egg()
            e.save()
            self.e = e

    def test_str(self):
        self.assertIsNot(str(self.e), "")
