# Generated by Django 3.0.5 on 2020-05-04 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chicken", "0004_auto_20200503_0030"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="egg",
            name="errors",
        ),
        migrations.AddField(
            model_name="egg",
            name="error",
            field=models.CharField(
                blank=True,
                choices=[("", "---"), ("W", "Windei"), ("Z", "Zerstört")],
                max_length=1,
                verbose_name="Fehler",
            ),
        ),
    ]
