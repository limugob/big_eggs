from django.contrib import admin
from django.contrib.sessions.models import Session

from big_eggs_auth.models import User


class SessionsAdmin(admin.ModelAdmin):
    list_display = ("session_key", "expire_date", "get_user")
    readonly_fields = ("get_decoded", "get_user")

    fields = (
        "session_key",
        "expire_date",
        "get_decoded",
        "get_user",
    )

    def get_user(self, object):
        if "_auth_user_id" in object.get_decoded():
            return User.objects.get(id=object.get_decoded()["_auth_user_id"])


admin.site.register(Session, SessionsAdmin)
