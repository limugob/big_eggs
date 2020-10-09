# Generated by Django 3.0.4 on 2020-04-14 10:10

from django.db import migrations, models

import chicken.models


class Migration(migrations.Migration):

    dependencies = [
        ("chicken", "0002_chicken_sex"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chicken",
            name="entry",
            field=models.DateTimeField(default=chicken.models.today_midnight),
        ),
        migrations.AlterField(
            model_name="chicken",
            name="sex",
            field=models.CharField(
                choices=[("U", "---"), ("W", "♀"), ("M", "♂")],
                default="U",
                max_length=1,
            ),
        ),
    ]
