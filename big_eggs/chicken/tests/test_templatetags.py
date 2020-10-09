from django.test import TestCase

from dateutil import relativedelta

from ..models import Chicken
from ..templatetags.chicken_utils import (
    relativedelta_to_str,
    to_bs_level,
    to_class_name,
)


class TagsTests(TestCase):
    def test_to_class_name(self):
        out = to_class_name(Chicken())
        self.assertEqual(out, "Huhn")

    def test_to_bs_level(self):
        out = to_bs_level(10)
        self.assertEqual(out, "secondary")

    def test_relativedelta_to_str(self):
        rd = relativedelta.relativedelta(years=2, months=1, days=20)
        out = relativedelta_to_str(rd)
        self.assertEqual(out, "2 Jahre, ein Monat, 20 Tage")
