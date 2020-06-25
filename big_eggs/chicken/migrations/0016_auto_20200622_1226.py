# Generated by Django 3.0.7 on 2020-06-22 10:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chicken", "0015_auto_20200622_1108"),
    ]

    operations = [
        migrations.AlterField(
            model_name="egg",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="chicken.ChickenGroup",
                verbose_name="Gruppe",
            ),
        ),
    ]