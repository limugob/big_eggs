# Generated by Django 3.0.7 on 2020-06-13 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tenants", "0002_auto_20200519_1429"),
        ("chicken", "0012_auto_20200613_1617"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="egg",
            unique_together={("tenant_id", "laid", "group", "chicken", "error")},
        ),
    ]
