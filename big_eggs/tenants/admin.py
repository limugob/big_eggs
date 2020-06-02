from django.contrib import admin
from django_scopes import scope, scopes_disabled

from .models import Tenant


class DisabledScopesMixin:
    pass
    # def get_form(self, request, obj=None, **kwargs):
    #     if object:
    #         with scope(tenant=obj.tenant_id):
    #             return super().get_form(request, obj=obj, **kwargs)
    #     with scopes_disabled():
    #         return super().get_form(request, obj, **kwargs)

    # def save_model(self, request, obj, form, change):
    #     with scope(tenant=obj.tenant_id):
    #         super().save_model(request, obj, form, change)

    # def get_queryset(self, request):
    #     with scopes_disabled():
    #         return super().get_queryset(request)


@admin.register(Tenant)
class TenantAdmin(DisabledScopesMixin, admin.ModelAdmin):
    filter_horizontal = ("users",)
