import django_filters
from django_scopes import scopes_disabled

from .models import Egg

with scopes_disabled():

    class EggFilter(django_filters.FilterSet):
        error = django_filters.ChoiceFilter(
            choices=Egg.Error.choices, empty_label="nicht filtern",
        )

        class Meta:
            model = Egg
            fields = ["error", "group"]
