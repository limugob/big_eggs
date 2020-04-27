from django.contrib import admin

from .models import Chicken, ChickenGroup, Egg


@admin.register(Chicken)
class ChickenAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'group', )
    fieldsets = (
        (None, {
            'fields': (
                ('number', 'name'), 
                ('sex', 'group'),
                ('entry', 'departure'),
                'note'
                )
        }),
    )

admin.site.register(ChickenGroup)
admin.site.register(Egg)


