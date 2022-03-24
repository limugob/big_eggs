# Generated by Django 3.0.5 on 2020-05-12 13:33

from django.db import migrations


def none_to_N(apps, schema_editor):
    """
    Egg.error must be a string with length 1.
    """
    Egg = apps.get_model("chicken", "Egg")
    updates = Egg.objects.filter(error="").update(error="N")
    print()
    print(f"Eggs updated: {updates}")


class Migration(migrations.Migration):

    dependencies = [
        ("chicken", "0005_auto_20200504_1631"),
    ]

    operations = [
        migrations.RunPython(none_to_N, elidable=True),
    ]
