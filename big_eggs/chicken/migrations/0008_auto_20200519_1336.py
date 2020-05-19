# Generated by Django 3.0.6 on 2020-05-19 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tenants", "0001_initial"),
        ("chicken", "0007_auto_20200512_1558"),
    ]

    operations = [
        migrations.AddField(
            model_name="chicken",
            name="tenant",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="tenants.Tenant",
            ),
        ),
        migrations.AddField(
            model_name="chickengroup",
            name="tenant",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="tenants.Tenant",
            ),
        ),
        migrations.AddField(
            model_name="egg",
            name="tenant",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="tenants.Tenant",
            ),
        ),
    ]