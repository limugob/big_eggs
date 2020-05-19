import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from tenants.models import Tenant


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        new_user = hasattr(self, "id")
        super().save(*args, **kwargs)

        if new_user:
            t = Tenant()
            t.save()
            t.users.add(self)
