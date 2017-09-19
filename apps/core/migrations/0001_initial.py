# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 19:30
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('post_code', models.CharField(max_length=30, verbose_name='Post code')),
                ('country', models.CharField(max_length=100, verbose_name='Country')),
                ('region', models.CharField(max_length=100, verbose_name='Region')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('street', models.CharField(max_length=150, verbose_name='Street')),
            ],
            options={
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.BinaryField()),
            ],
            options={
                'db_table': 'attachment',
            },
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('diagnosis', models.TextField()),
                ('diagnosis_date', models.DateField()),
            ],
            options={
                'db_table': 'diagnosis',
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'doctor',
            },
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=70, verbose_name='Hospital Name')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Address')),
            ],
            options={
                'db_table': 'hospital',
            },
        ),
        migrations.CreateModel(
            name='IntInd',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('view_name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('min_norm', models.IntegerField(blank=True, null=True)),
                ('max_norm', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'int_ind',
            },
        ),
        migrations.CreateModel(
            name='MedArea',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('view_name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.MedArea')),
            ],
            options={
                'db_table': 'med_area',
            },
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('summary', models.CharField(max_length=255)),
                ('info', models.TextField(blank=True, null=True)),
                ('drugs', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('medication_date', models.DateField()),
            ],
            options={
                'db_table': 'medication',
            },
        ),
        migrations.CreateModel(
            name='MedTest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('view_name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('med_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.MedArea')),
            ],
            options={
                'db_table': 'med_test',
            },
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hospital', models.ManyToManyField(to='core.Hospital')),
            ],
            options={
                'db_table': 'nurse',
            },
        ),
        migrations.CreateModel(
            name='OmiCard',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.CharField(max_length=16, verbose_name='Number')),
                ('expire_date', models.DateField(verbose_name='Expiration date')),
                ('insurance_org', models.CharField(max_length=150, verbose_name='Insurance Organization')),
            ],
            options={
                'db_table': 'omi_card',
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('series', models.CharField(max_length=4, verbose_name='Series')),
                ('number', models.CharField(max_length=6, verbose_name='Number')),
                ('issue_date', models.DateField(verbose_name='Issue date')),
                ('authority_code', models.CharField(max_length=30, verbose_name='Authority Code')),
                ('authority', models.CharField(max_length=100, verbose_name='Authority')),
                ('issue_place', models.CharField(max_length=150, verbose_name='Issue Place')),
            ],
            options={
                'db_table': 'passport',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gender', models.CharField(choices=[('MALE', 'мужской'), ('FEMALE', 'женский')], max_length=20)),
                ('blood_group', models.CharField(blank=True, choices=[('I', 'первая'), ('II', 'вторая'), ('III', 'третья'), ('IV', 'четвертая')], max_length=20, null=True)),
                ('rh_factor', models.CharField(blank=True, choices=[('positive', 'Rh+'), ('negative', 'Rh-')], max_length=20, null=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('omi_card', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.OmiCard')),
                ('passport', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Passport')),
            ],
            options={
                'db_table': 'patient',
            },
        ),
        migrations.CreateModel(
            name='RealInd',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('view_name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('min_norm', models.FloatField(blank=True, null=True)),
                ('max_norm', models.FloatField(blank=True, null=True)),
                ('med_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.MedTest')),
            ],
            options={
                'db_table': 'real_ind',
            },
        ),
        migrations.CreateModel(
            name='TestRec',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('real_indicators', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('int_indicators', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('text_indicators', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('info', models.TextField(blank=True, null=True)),
                ('test_date', models.DateField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Patient')),
            ],
            options={
                'db_table': 'test_rec',
            },
        ),
        migrations.CreateModel(
            name='TextInd',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('view_name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('values', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None)),
                ('med_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.MedTest')),
            ],
            options={
                'db_table': 'text_ind',
            },
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('finish_date', models.DateField()),
                ('summary', models.CharField(max_length=255)),
                ('info', models.TextField(blank=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Patient')),
            ],
            options={
                'db_table': 'treatment',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('surname', models.CharField(max_length=50, verbose_name='Surname')),
                ('patronymic', models.CharField(blank=True, max_length=50, null=True, verbose_name='Patronymic')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Username')),
                ('password', models.CharField(max_length=16, verbose_name='Password')),
                ('phone', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), blank=True, null=True, size=None, verbose_name='Phone')),
                ('email', django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=30), blank=True, null=True, size=None, verbose_name='Email')),
                ('creation_ts', models.DateTimeField(verbose_name='Creation datetime')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='user_account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nurse',
            name='user_account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medication',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Patient'),
        ),
        migrations.AddField(
            model_name='intind',
            name='med_test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.MedTest'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='hospital',
            field=models.ManyToManyField(to='core.Hospital'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='user_account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Patient'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='test_record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.TestRec'),
        ),
    ]
