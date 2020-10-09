import django_filters
from django.db.models import Q
from django_filters.filters import CharFilter
from django_filters.views import FilterView
from django_scopes import scopes_disabled

from .models import Chicken, ChickenGroup, Egg


def tenant_groups(request):
    if request is None:
        ChickenGroup.objects.none()
    return ChickenGroup.objects.all()


def selectable_tenant_groups(request):
    return tenant_groups(request).filter(selectable=True)


class EggFilter(django_filters.FilterSet):
    group = django_filters.ModelChoiceFilter(queryset=selectable_tenant_groups)

    error = django_filters.ChoiceFilter(
        choices=Egg.Error.choices, empty_label="nicht filtern",
    )

    size = django_filters.ChoiceFilter(
        choices=Egg.Size.choices, empty_label="nicht filtern",
    )

    class Meta:
        model = Egg
        fields = ["group", "size", "error"]


with scopes_disabled():

    class ChickenFilter(django_filters.FilterSet):
        name = django_filters.CharFilter(method="name_filter")
        group = django_filters.ModelChoiceFilter(queryset=tenant_groups)
        in_stock = django_filters.BooleanFilter(
            field_name="departure",
            lookup_expr="isnull",
            label="Im Bestand",
            required=True,
        )
        sex = django_filters.ChoiceFilter(
            choices=Chicken.SEX_CHOICES, empty_label="nicht filtern"
        )

        def name_filter(self, queryset, name, value):
            return queryset.filter(
                Q(name__icontains=value)
                | Q(group__name__icontains=value)
                | Q(number__icontains=value)
            )

        class Meta:
            model = Chicken
            fields = ["name", "group", "in_stock", "sex"]

    class ChickenFilterView(FilterView):
        filterset_class = ChickenFilter

        def get_filterset_kwargs(self, filterset_class):
            """ Set default filters
            """
            kwargs = super().get_filterset_kwargs(filterset_class)
            if kwargs["data"] is None:
                kwargs["data"] = {"in_stock": True}
            return kwargs
