# Generated by Django 3.0.4 on 2020-03-21 23:10

import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import chicken.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chicken",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("number", models.CharField(blank=True, max_length=60)),
                ("name", models.CharField(blank=True, max_length=60)),
                ("entry", models.DateTimeField(default=django.utils.timezone.now)),
                ("departure", models.DateTimeField(blank=True, null=True)),
                ("note", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="ChickenGroup",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name="Egg",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("laid", models.DateTimeField(default=chicken.models.today_midnight)),
                (
                    "chicken",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="chicken.Chicken",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="chicken.ChickenGroup",
                    ),
                ),
            ],
            options={
                "verbose_name": "Egg",
                "verbose_name_plural": "Eggs",
                "ordering": ("-laid",),
            },
        ),
        migrations.AddField(
            model_name="chicken",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="chicken.ChickenGroup",
            ),
        ),
    ]
