from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.postgres.fields import *
from django.core.exceptions import ValidationError
from django.db import models

GENDER = (
    ('MALE', 'мужской'),
    ('FEMALE', 'женский')
)

BLOOD_GROUP = (
    ('I', 'первая'),
    ('II', 'вторая'),
    ('III', 'третья'),
    ('IV', 'четвертая')
)

RH_FACTOR = (
    ('positive', 'Rh+'),
    ('negative', 'Rh-')
)


class AbstractModel(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


class Address(AbstractModel):
    post_code = models.CharField(max_length=30, verbose_name='Post code')
    country = models.CharField(max_length=100, verbose_name='Country')
    region = models.CharField(max_length=100, verbose_name='Region')
    city = models.CharField(max_length=100, verbose_name='City')
    street = models.CharField(max_length=150, verbose_name='Street')

    class Meta:
        db_table = 'address'


class OmiCard(AbstractModel):
    number = models.CharField(max_length=16, verbose_name='Number')
    expire_date = models.DateField(verbose_name='Expiration date')
    insurance_org = models.CharField(max_length=150, verbose_name='Insurance Organization')

    class Meta:
        db_table = 'omi_card'


class Passport(AbstractModel):
    series = models.CharField(max_length=4, verbose_name='Series')
    number = models.CharField(max_length=6, verbose_name='Number')
    issue_date = models.DateField(verbose_name='Issue date')
    authority_code = models.CharField(max_length=30, verbose_name='Authority Code')
    authority = models.CharField(max_length=100, verbose_name='Authority')
    issue_place = models.CharField(max_length=150, verbose_name='Issue Place')

    class Meta:
        db_table = 'passport'


class Hospital(AbstractModel):
    name = models.CharField(max_length=70, verbose_name='Hospital Name')
    address = models.OneToOneField('core.Address')

    class Meta:
        db_table = 'hospital'


class User(AbstractModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Name')
    surname = models.CharField(max_length=50, verbose_name='Surname')
    patronymic = models.CharField(max_length=50, blank=True, null=True, verbose_name='Patronymic')
    username = models.CharField(max_length=30, verbose_name='Username', unique=True)
    password = models.CharField(max_length=16, verbose_name='Password')
    phone = ArrayField(models.CharField(max_length=30), blank=True, null=True, verbose_name='Phone')
    email = ArrayField(models.EmailField(max_length=30), blank=True, null=True, verbose_name='Email')
    creation_ts = models.DateTimeField(verbose_name='Creation datetime')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    class Meta:
        db_table = 'user'


class Patient(AbstractModel):
    user_account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=GENDER)
    blood_group = models.CharField(max_length=20, choices=BLOOD_GROUP, blank=True, null=True)
    rh_factor = models.CharField(max_length=20, choices=RH_FACTOR, blank=True, null=True)
    is_disabled = models.BooleanField(default=False)
    omi_card = models.OneToOneField('core.OmiCard', blank=True, null=True)
    passport = models.OneToOneField('core.Passport', blank=True, null=True)

    class Meta:
        db_table = 'patient'


class MedicalEmployee(AbstractModel):
    user_account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hospital = models.ManyToManyField('core.Hospital')

    class Meta:
        abstract = True


class Doctor(MedicalEmployee):
    class Meta:
        db_table = 'doctor'


class Nurse(MedicalEmployee):
    class Meta:
        db_table = 'nurse'


class MedArea(AbstractModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('core.MedArea', blank=True, null=True)

    class Meta:
        db_table = 'med_area'


class MedTest(AbstractModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True, null=True)
    med_area = models.ForeignKey('core.MedArea')

    class Meta:
        db_table = 'med_test'


class Ind(AbstractModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True, null=True)
    med_test = models.ForeignKey('core.MedTest')

    class Meta:
        abstract = True


class RealInd(Ind):
    min_norm = models.FloatField(blank=True, null=True)
    max_norm = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'real_ind'

    def save(self, *args, **kwargs):
        if self.min_norm > self.max_norm:
            raise ValidationError("Min norm must be less than max norm")
        super(RealInd, self).save()


class IntInd(Ind):
    min_norm = models.IntegerField(blank=True, null=True)
    max_norm = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'int_ind'

    def save(self, *args, **kwargs):
        if self.min_norm > self.max_norm:
            raise ValidationError("Min norm must be less than max norm")
        super(IntInd, self).save()


class TextInd(Ind):
    values = ArrayField(models.CharField(max_length=255), null=True, blank=True)

    class Meta:
        db_table = 'text_ind'


class TestRec(AbstractModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True, null=True)
    real_indicators = JSONField(blank=True, null=True)
    int_indicators = JSONField(blank=True, null=True)
    text_indicators = JSONField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    test_date = models.DateField()
    patient = models.ForeignKey('core.Patient', on_delete=models.CASCADE)

    class Meta:
        db_table = 'test_rec'


class Attachment(AbstractModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True, null=True)
    content = models.BinaryField()
    test_record = models.ForeignKey('core.TestRec')

    class Meta:
        db_table = 'attachment'


class Treatment(AbstractModel):
    start_date = models.DateField()
    finish_date = models.DateField()
    summary = models.CharField(max_length=255)
    info = models.TextField(blank=True, null=True)
    patient = models.ForeignKey('core.Patient', on_delete=models.CASCADE)

    class Meta:
        db_table = 'treatment'


class Medication(AbstractModel):
    summary = models.CharField(max_length=255)
    info = models.TextField(blank=True, null=True)
    drugs = ArrayField(models.CharField(max_length=100))
    medication_date = models.DateField()
    patient = models.ForeignKey('core.Patient', on_delete=models.CASCADE)

    class Meta:
        db_table = 'medication'


class Diagnosis(AbstractModel):
    diagnosis = models.TextField()
    diagnosis_date = models.DateField()
    patient = models.ForeignKey('core.Patient', on_delete=models.CASCADE)

    class Meta:
        db_table = 'diagnosis'
