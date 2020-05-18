from django.contrib import admin

from .models import Chicken, ChickenGroup, Egg
from .templatetags.chicken_utils import relativedelta_to_str


@admin.register(Chicken)
class ChickenAdmin(admin.ModelAdmin):
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
                    ("number", "name"),
                    ("sex", "group"),
                    ("hatching", "age_display"),
                    ("entry", "departure"),
                    "note",
                )
            },
        ),
    )

    def age_display(self, object):
        return relativedelta_to_str(object.age())


admin.site.register(ChickenGroup)
admin.site.register(Egg)
