import uuid

from django.db import models


class Tenant(models.Model):
    users = models.ManyToManyField("big_eggs_auth.User")


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TenantDataModel(UUIDModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    class Meta:
        abstract = True
