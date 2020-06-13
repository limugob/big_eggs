# Generated by Django 3.0.7 on 2020-06-13 14:17

from django.db import migrations
from django.db.models import Sum
from django_scopes import scopes_disabled


def fill_egg_quantity(apps, scheme_editor):
    Egg = apps.get_model("chicken", "Egg")

    with scopes_disabled():
        deletion_list = list(Egg.objects.values_list("id", flat=True))
        entries = Egg.objects.values("laid", "group_id", "error", "tenant_id").annotate(
            eggs_count=Sum("quantity")
        )
        for entry in entries:
            Egg.objects.create(
                laid=entry["laid"],
                group_id=entry["group_id"],
                error=entry["error"],
                tenant_id=entry["tenant_id"],
                quantity=entry["eggs_count"],
            )
        print()
        print("Entries deleted: ", Egg.objects.filter(id__in=deletion_list).delete())


class Migration(migrations.Migration):

    dependencies = [
        ("chicken", "0011_egg_quantity"),
    ]

    operations = [
        migrations.RunPython(fill_egg_quantity),
    ]