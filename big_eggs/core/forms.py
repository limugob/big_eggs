import datetime

from django import forms
from django.utils import timezone


class DateOnlyField(forms.DateField):
    widget = forms.TextInput(attrs={"type": "date", "min": 1, "step": 1,})

    def prepare_value(self, value):
        if isinstance(value, datetime.datetime):
            return timezone.localdate(value)
        return value  # when errors occurs, return unchanged

    def to_python(self, value):
        value_as_date = super().to_python(value)
        if value_as_date is None:
            return None
        return timezone.make_aware(
            datetime.datetime.combine(value_as_date, datetime.datetime.min.time())
        )


class CheckedRadioSelect(forms.widgets.RadioSelect):
    option_template_name = "big_eggs/widgets/radio_option.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "class" in self.attrs:
            self.attrs["class"] += " checked-radio"
        else:
            self.attrs["class"] = "checked-radio"
