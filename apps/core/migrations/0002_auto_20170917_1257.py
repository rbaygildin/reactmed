# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-17 12:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='intind',
            table='int_ind',
        ),
        migrations.AlterModelTable(
            name='realind',
            table='real_ind',
        ),
    ]