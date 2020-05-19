import uuid

from django.db import models
from django_scopes import ScopedManager, get_scope, scopes_disabled


class Tenant(models.Model):
    users = models.ManyToManyField("big_eggs_auth.User")


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TenantDataModel(UUIDModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    objects = ScopedManager(tenant="tenant")

    class Meta:
        abstract = True

    def validate_unique(self, *args, **kwargs):
        with scopes_disabled():
            super().validate_unique(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.tenant_id = get_scope()["tenant"]
        super().save(*args, **kwargs)
