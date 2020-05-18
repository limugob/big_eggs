import django_filters

from .models import Egg


class EggFilter(django_filters.FilterSet):
    error = django_filters.ChoiceFilter(
        choices=Egg.Error.choices, empty_label="nicht filtern",
    )

    class Meta:
        model = Egg
        fields = ["error", "group"]
