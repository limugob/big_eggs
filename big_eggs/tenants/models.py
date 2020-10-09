import uuid

from django.db import models

from django_scopes import ScopedManager, get_scope, scopes_disabled


class Tenant(models.Model):
    users = models.ManyToManyField("big_eggs_auth.User")
    name = models.CharField(max_length=60, blank=True)

    def __str__(self):
        out = f"T {self.id}"
        if self.name:
            out += f" - {self.name}"
        return out


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
        if not self.tenant_id:
            self.tenant_id = get_scope()["tenant"]
        super().save(*args, **kwargs)
