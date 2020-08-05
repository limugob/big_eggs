from django.contrib import admin

from tenants.admin import DisabledScopesMixin

from .models import Chicken, ChickenGroup, Egg
from .templatetags.chicken_utils import relativedelta_to_str


@admin.register(Chicken)
class ChickenAdmin(DisabledScopesMixin, admin.ModelAdmin):
    list_display = (
        "__str__",
        "group",
    )
    readonly_fields = ("age_display",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("tenant"),
                    ("number", "name"),
                    ("sex", "group"),
                    ("hatching", "age_display"),
                    ("entry", "departure"),
                    "note",
                )
            },
        ),
    )
    list_filter = ("tenant",)

    def age_display(self, object):
        return relativedelta_to_str(object.age())


class CommonAdmin(DisabledScopesMixin, admin.ModelAdmin):

    list_filter = ("tenant",)


@admin.register(Egg)
class EggsAdmin(CommonAdmin):
    list_select_related = ("group",)


admin.site.register(ChickenGroup, CommonAdmin)
