# Generated by Django 3.0.7 on 2020-06-15 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chicken", "0013_auto_20200613_1652"),
    ]

    operations = [
        migrations.AddField(
            model_name="chickengroup",
            name="selectable",
            field=models.BooleanField(
                default=True, help_text="Group selectable in egg input form?"
            ),
        ),
    ]
