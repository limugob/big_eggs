# Generated by Django 3.0.6 on 2020-05-19 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tenants", "0001_initial"),
        ("chicken", "0009_auto_20200519_1337"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chicken",
            name="tenant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tenants.Tenant"
            ),
        ),
        migrations.AlterField(
            model_name="chickengroup",
            name="tenant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tenants.Tenant"
            ),
        ),
        migrations.AlterField(
            model_name="egg",
            name="tenant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tenants.Tenant"
            ),
        ),
    ]
