# Generated by Django 3.0.5 on 2020-05-12 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chicken", "0006_auto_20200512_1533"),
    ]

    operations = [
        migrations.AlterField(
            model_name="egg",
            name="error",
            field=models.CharField(
                choices=[("N", "keine"), ("W", "Windei"), ("Z", "Zerstört")],
                default="N",
                max_length=1,
                verbose_name="Fehler",
            ),
        ),
    ]
