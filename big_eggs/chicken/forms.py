from django import forms
from django.utils import timezone
from django_scopes.forms import SafeModelChoiceField

from .models import Chicken, ChickenGroup, Egg


def get_chicken_group_choices():
    return [(None, "---")] + list(
        ChickenGroup.objects.values_list("id", "name").order_by("name")
    )


def today_date():
    return timezone.localdate(timezone.now())


class EggBulkForm(forms.Form):
    date = forms.DateField(
        initial=today_date,
        widget=forms.TextInput(attrs={"type": "date", "min": 1, "step": 1,}),
        label="Datum",
    )
    count = forms.IntegerField(min_value=1, initial=1, label="Anzahl",)
    group = forms.ChoiceField(
        initial=None, choices=get_chicken_group_choices, required=False, label="Gruppe",
    )
    error = forms.ChoiceField(
        initial="", required=False, label="Fehler", choices=Egg.Error.choices,
    )


class ChickenForm(forms.ModelForm):
    hatching_date = forms.DateField(
        initial=today_date,
        widget=forms.TextInput(attrs={"type": "date", "min": 1, "step": 1,}),
        label="Schlupf",
    )
    entry_date = forms.DateField(
        initial=today_date,
        widget=forms.TextInput(attrs={"type": "date", "min": 1, "step": 1,}),
        label="Zugang",
    )
    departure_date = forms.DateField(
        widget=forms.TextInput(attrs={"type": "date", "min": 1, "step": 1,}),
        label="Abgang",
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        if (
            cleaned_data["departure_date"]
            and cleaned_data["entry_date"] > cleaned_data["departure_date"]
        ):
            raise forms.ValidationError(
                {"departure_date": "Abgang kann nicht vor Zugang liegen."}
            )
        if cleaned_data["hatching_date"] > cleaned_data["entry_date"]:
            raise forms.ValidationError(
                {"entry_date": "Zugang kann nicht vor Schlupf liegen."}
            )
        return cleaned_data

    class Meta:
        model = Chicken
        fields = [
            "number",
            "name",
            "group",
            "sex",
            "hatching_date",
            "entry_date",
            "departure_date",
            "note",
        ]
        field_classes = {
            "group": SafeModelChoiceField,
        }
