import datetime

from django import forms
from django.utils import timezone


class DateInputWithArrows(forms.widgets.DateInput):
    template_name = "big_eggs/widgets/input_with_arrows.html"
    input_type = "date"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs["min"] = 1
        self.attrs["step"] = 1
        self.attrs["autocomplete"] = "off"


class DateOnlyField(forms.DateField):
    widget = DateInputWithArrows

    def prepare_value(self, value):
        if isinstance(value, datetime.datetime):
            return timezone.localdate(value).isoformat()
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


class NumberInputWithArrows(forms.widgets.NumberInput):
    template_name = "big_eggs/widgets/input_with_arrows.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs["autocomplete"] = "off"
        self.attrs["min"] = 1
