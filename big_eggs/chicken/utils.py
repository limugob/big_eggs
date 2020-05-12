from django.utils import timezone

def today_midnight():
    return timezone.localtime(timezone.now()).replace(hour=0, minute=0, second=0, microsecond=0)
