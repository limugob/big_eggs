# Generated by Django 3.0.5 on 2020-05-02 22:30

import chicken.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chicken', '0003_auto_20200414_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='chicken',
            name='hatching',
            field=models.DateTimeField(default=chicken.models.today_midnight, verbose_name='Schlupf'),
        ),
        migrations.AddField(
            model_name='egg',
            name='errors',
            field=models.CharField(blank=True, choices=[('W', 'Windei'), ('Z', 'Zerstört')], max_length=1, verbose_name='Fehler'),
        ),
        migrations.AlterField(
            model_name='chicken',
            name='departure',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Abgang'),
        ),
        migrations.AlterField(
            model_name='chicken',
            name='entry',
            field=models.DateTimeField(default=chicken.models.today_midnight, verbose_name='Zugang'),
        ),
        migrations.AlterField(
            model_name='chicken',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chicken.ChickenGroup', verbose_name='Gruppe'),
        ),
        migrations.AlterField(
            model_name='chicken',
            name='note',
            field=models.TextField(blank=True, verbose_name='Notizen'),
        ),
        migrations.AlterField(
            model_name='chicken',
            name='number',
            field=models.CharField(blank=True, max_length=60, verbose_name='Ringnummer'),
        ),
        migrations.AlterField(
            model_name='chicken',
            name='sex',
            field=models.CharField(choices=[('U', '---'), ('W', '♀'), ('M', '♂')], default='U', max_length=1, verbose_name='Geschlecht'),
        ),
    ]