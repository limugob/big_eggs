from django.contrib import admin
from django.contrib.sessions.models import Session


class SessionsAdmin(admin.ModelAdmin):
    list_display = (
        "session_key",
        "expire_date",
    )
    readonly_fields = ("get_decoded",)

    fields = (
        "session_key",
        "expire_date",
        "get_decoded",
    )


admin.site.register(Session, SessionsAdmin)
