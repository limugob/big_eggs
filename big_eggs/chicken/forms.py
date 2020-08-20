from django import forms
from django.utils import timezone
from django_scopes.forms import SafeModelChoiceField

from core.forms import CheckedRadioSelect, DateOnlyField

from .models import Chicken, ChickenGroup, Egg


def today_date():
    return timezone.localdate(timezone.now())


class EggBulkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["laid"].initial = today_date
        chickengroups = ChickenGroup.objects.filter(selectable=True)
        self.fields["group"].queryset = chickengroups
        # if len(chickengroups) < 5:
        # self.fields["group"].widget = forms.RadioSelect()

    class Meta:
        model = Egg
        fields = [
            "laid",
            "quantity",
            "group",
            "size",
            "error",
        ]
        field_classes = {
            "laid": DateOnlyField,
            "group": SafeModelChoiceField,
        }
        widgets = {
            "group": CheckedRadioSelect,
            "size": CheckedRadioSelect,
        }


class ChickenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"].queryset = ChickenGroup.objects.all()

    class Meta:
        model = Chicken
        fields = [
            "number",
            "name",
            "group",
            "sex",
            "hatching",
            "entry",
            "departure",
            "note",
        ]
        field_classes = {
            "group": SafeModelChoiceField,
            "hatching": DateOnlyField,
            "entry": DateOnlyField,
            "departure": DateOnlyField,
        }
