# Generated by Django 3.0.7 on 2020-06-26 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tenants", "0002_auto_20200519_1429"),
    ]

    operations = [
        migrations.AddField(
            model_name="tenant",
            name="name",
            field=models.CharField(blank=True, max_length=60),
        ),
    ]