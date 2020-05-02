from django import forms
from django.utils import timezone

from .models import ChickenGroup, Chicken


def get_chicken_group_choices():
    return [(None, '---')] + list(ChickenGroup.objects.values_list('id', 'name').order_by('name'))


def today_date():
    return timezone.localdate(timezone.now())

class EggBulkForm(forms.Form):
    date = forms.DateField(
        initial=today_date,
        widget=forms.TextInput(attrs={
            'type': 'date',
            'min': 1,
            'step': 1,
        }),
        label='Datum',
    )
    count = forms.IntegerField(
        min_value=1,
        initial=1,
        label='Anzahl',
    )
    group = forms.ChoiceField(
        initial=None,
        choices=get_chicken_group_choices,
        required=False,
        label='Gruppe',
    )


class ChickenForm(forms.ModelForm):
    entry_date = forms.DateField(
        initial=today_date,
        widget=forms.TextInput(attrs={
            'type': 'date',
            'min': 1,
            'step': 1,
        }),
        label='Zugang',
    )
    departure_date = forms.DateField(
        widget=forms.TextInput(attrs={
            'type': 'date',
            'min': 1,
            'step': 1,
        }),
        label='Abgang',
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['departure_date'] and cleaned_data['entry_date'] > cleaned_data['departure_date']:
            raise forms.ValidationError({
                'departure_date': 'Abgang kann nicht vor Zugang liegen.'
            })




    class Meta:
        model = Chicken
        fields = [
            'number', 'name', 'group', 
            'group', 'sex',
            'entry_date', 'departure_date',
            'note']

