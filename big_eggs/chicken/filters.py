import django_filters

from .models import ChickenGroup, Egg


def tenant_groups(request):
    if request is None:
        ChickenGroup.objects.none()
    return ChickenGroup.objects.all()


class EggFilter(django_filters.FilterSet):
    group = django_filters.ModelChoiceFilter(queryset=tenant_groups)

    error = django_filters.ChoiceFilter(
        choices=Egg.Error.choices, empty_label="nicht filtern",
    )

    class Meta:
        model = Egg
        fields = ["group", "error"]
