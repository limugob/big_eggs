from django.contrib import admin
from django_scopes import scopes_disabled

from .models import Tenant


class DisabledScopesMixin:
    def get_queryset(self, request):
        with scopes_disabled():
            return super().get_queryset(request)


@admin.register(Tenant)
class TenantAdmin(DisabledScopesMixin, admin.ModelAdmin):
    filter_horizontal = ("users",)
