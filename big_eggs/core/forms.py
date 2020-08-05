import datetime

from django import forms
from django.utils import timezone


class DateOnlyField(forms.DateField):
    widget = forms.TextInput(attrs={"type": "date", "min": 1, "step": 1,})

    def to_python(self, value):
        value_as_date = super().to_python(value)
        return timezone.make_aware(
            datetime.datetime.combine(value_as_date, datetime.datetime.min.time())
        )
