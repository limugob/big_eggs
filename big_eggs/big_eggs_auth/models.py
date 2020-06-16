import uuid

from django.contrib.auth.models import AbstractUser
from django.core.mail import mail_admins
from django.db import models

from tenants.models import Tenant


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.tenant_set.count() == 0:
            t = Tenant()
            t.save()
            t.users.add(self)
            mail_admins("New User: " + self.email, "")

    @property
    def tenant(self):
        return self.tenant_set.first()

    @property
    def tenant_id(self):
        return self.tenant_set.first().id
