# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 20:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20171015_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnosis',
            name='complications',
            field=models.TextField(blank=True, null=True, verbose_name='Осложнения'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='diagnosis_type',
            field=models.CharField(choices=[('Предварительный', 'Предварительный'), ('Клинический', 'Клинический'), ('Окончательный', 'Окончательный')], default='Предварительный', max_length=30, verbose_name='Вид диагноза по времени'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='info',
            field=models.TextField(blank=True, null=True, verbose_name='Информация'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='other_diseases',
            field=models.TextField(blank=True, null=True, verbose_name='Сопуствующие заболевания'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='summary',
            field=models.TextField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='diagnosis',
            field=models.CharField(max_length=300, verbose_name='Диагноз'),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnosis', to='core.Patient', verbose_name='Пациент'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 17, 20, 8, 32, 729762, tzinfo=utc)),
        ),
    ]