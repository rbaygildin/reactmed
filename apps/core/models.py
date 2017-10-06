from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import *
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import date, timedelta

from transliterate import translit

from apps.core.managers import UserManager

GENDER = (
    ('Мужской', 'мужской'),
    ('Женский', 'женский')
)

BLOOD_GROUP = (
    ('I', 'I'),
    ('II', 'II'),
    ('III', 'III'),
    ('IV', 'IV')
)

RH_FACTOR = (
    ('Rh+', 'Rh+'),
    ('Rh-', 'Rh-')
)


class AbstractModel(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(verbose_name=_('Email'), max_length=30, unique=True)
    name = models.CharField(verbose_name=_('Name'), max_length=30)
    surname = models.CharField(verbose_name=_('Surname'), max_length=30)
    patronymic = models.CharField(verbose_name=_('Patronymic'), max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(_('Is Staff'), default=False)
    date_joined = models.DateTimeField(default=timezone.now())

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_short_name(self):
        return '%s %s' % (self.name, self.surname)

    def get_full_name(self):
        return '%s' % self.name


class Address(AbstractModel):
    post_code = models.CharField(max_length=30, verbose_name='Post code')
    country = models.CharField(max_length=100, verbose_name='Country')
    region = models.CharField(max_length=100, verbose_name='Region')
    city = models.CharField(max_length=100, verbose_name='City')
    street = models.CharField(max_length=150, verbose_name='Street')

    class Meta:
        db_table = 'address'
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')


class OmiCard(AbstractModel):
    number = models.CharField(max_length=16, verbose_name='Number')
    expire_date = models.DateField(verbose_name='Expiration date')
    insurance_org = models.CharField(max_length=150, verbose_name='Insurance Organization')

    class Meta:
        db_table = 'omi_card'
        verbose_name = _('OMI Card')
        verbose_name_plural = _('OMI Cards')


# class Passport(AbstractModel):
#     series = models.CharField(max_length=4, verbose_name='Series')
#     number = models.CharField(max_length=6, verbose_name='Number')
#     issue_date = models.DateField(verbose_name='Issue date')
#     authority_code = models.CharField(max_length=30, verbose_name='Authority Code')
#     authority = models.CharField(max_length=100, verbose_name='Authority')
#     issue_place = models.CharField(max_length=150, verbose_name='Issue Place')
#
#     class Meta:
#         db_table = 'passport'
#         verbose_name = _('Passport')
#         verbose_name_plural = _('Passports')


# class Hospital(AbstractModel):
#     name = models.CharField(max_length=70, verbose_name='Hospital Name')
#     address = models.OneToOneField('core.Address')
#
#     class Meta:
#         db_table = 'hospital'
#         verbose_name = _('Hospital')
#         verbose_name_plural = _('Hospitals')


class Patient(AbstractModel):
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    surname = models.CharField(verbose_name=_('Surname'), max_length=50)
    patronymic = models.CharField(verbose_name=_('Patronymic'), max_length=50, blank=True, null=True)
    gender = models.CharField(verbose_name=_('Gender'), max_length=20, choices=GENDER)
    birthday = models.DateField(verbose_name=_('Birthday'))
    blood_group = models.CharField(verbose_name=_('Blood Group'), max_length=20, choices=BLOOD_GROUP, blank=True,
                                   null=True)
    rh_factor = models.CharField(verbose_name=_('RH Factor'), max_length=20, choices=RH_FACTOR, blank=True, null=True)
    is_disabled = models.BooleanField(verbose_name=_('Disabled'), default=False)
    omi_card = models.CharField(verbose_name=_('OMI Card'), max_length=16, blank=True, null=True)
    address = models.CharField(verbose_name=_('Address'), max_length=255, blank=True, null=True)
    occupation = models.CharField(verbose_name=_('Occupation'), max_length=100, blank=True, null=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='patients', on_delete=models.CASCADE)

    @property
    def age(self):
        return (date.today() - self.birthday) // timedelta(days=365.2425)

    class Meta:
        db_table = 'patient'
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')


#
# class MedicalEmployee(AbstractModel):
#     user_account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     hospital = models.ManyToManyField('core.Hospital')
#
#     class Meta:
#         abstract = True
#
#
# class Doctor(MedicalEmployee):
#     class Meta:
#         db_table = 'doctor'
#
#
# class Nurse(MedicalEmployee):
#     class Meta:
#         db_table = 'nurse'


class BaseMedType(AbstractModel):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200, unique=True, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class MedArea(BaseMedType):
    parent = models.ForeignKey('core.MedArea', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.short_name is None or self.short_name == '':
            self.short_name = translit(self.name, 'ru', reversed=True).lower().replace(' ', '_')
        super(MedArea, self).save(*args, **kwargs)

    class Meta:
        db_table = 'med_area'
        verbose_name = _('Medical Area')
        verbose_name_plural = _('Medical Areas')


class MedTest(BaseMedType):
    med_area = models.ForeignKey('core.MedArea')

    def save(self, *args, **kwargs):
        if self.short_name is None or self.short_name == '':
            self.short_name = self.med_area.short_name + '_' + translit(self.name, 'ru', reversed=True).lower().replace(' ', '_')
        super(MedTest, self).save(*args, **kwargs)

    class Meta:
        db_table = 'med_test'
        verbose_name = _('Medical Test')
        verbose_name_plural = _('Medical Tests')


class RealInd(BaseMedType):
    med_test = models.ForeignKey('core.MedTest', related_name='real_inds')
    min_norm = models.FloatField(blank=True, null=True)
    max_norm = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'real_ind'
        verbose_name = _('Real Indicator')
        verbose_name_plural = _('Real Indicators')

    def save(self, *args, **kwargs):
        if self.min_norm is None or self.max_norm is None:
            pass
        elif self.min_norm > self.max_norm:
            raise ValidationError("Min norm must be less than max norm")
        if self.short_name is None or self.short_name == '':
            self.short_name = self.med_test.short_name + '_' + translit(self.name, 'ru', reversed=True).lower().replace(' ', '_')
        super(RealInd, self).save(*args, **kwargs)


class IntInd(BaseMedType):
    med_test = models.ForeignKey('core.MedTest', related_name='int_inds')
    min_norm = models.IntegerField(blank=True, null=True)
    max_norm = models.IntegerField(blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'int_ind'
        verbose_name = _('Integer Indicator')
        verbose_name_plural = _('Integer Indicators')

    def save(self, *args, **kwargs):
        if self.min_norm is None or self.max_norm is None:
            pass
        elif self.min_norm > self.max_norm:
            raise ValidationError("Min norm must be less than max norm")
        if self.short_name is None or self.short_name == '':
            self.short_name = self.med_test.short_name + '_' + translit(self.name, 'ru', reversed=True).lower().replace(' ', '_')
        super(IntInd, self).save(*args, **kwargs)


class TextInd(BaseMedType):
    med_test = models.ForeignKey('core.MedTest', related_name='text_inds')
    values = ArrayField(models.CharField(max_length=255), null=True, blank=True)

    class Meta:
        db_table = 'text_ind'
        verbose_name = _('Text Indicator')
        verbose_name_plural = _('Text Indicators')

    def save(self, *args, **kwargs):
        if self.short_name is None or self.short_name == '':
            self.short_name = self.med_test.short_name + '_' + translit(self.name, 'ru', reversed=True).lower().replace(' ', '_')
        super(TextInd, self).save(*args, **kwargs)


class TestRec(AbstractModel):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True, null=True)
    real_inds = JSONField(blank=True, null=True)
    int_inds = JSONField(blank=True, null=True)
    text_inds = JSONField(blank=True, null=True)
    summary = models.CharField(max_length=100, blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    test_date = models.DateField()
    patient = models.ForeignKey('core.Patient', on_delete=models.CASCADE, related_name='test_recs')

    class Meta:
        db_table = 'test_rec'
        verbose_name = _('Test Record')
        verbose_name_plural = _('Test Records')


class Attachment(AbstractModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True, null=True)
    content = models.BinaryField()
    test_record = models.ForeignKey('core.TestRec')

    class Meta:
        db_table = 'attachment'
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')


# class Appointment(AbstractModel):
#     appointment_date = models.DateTimeField()
#     info = models.DateTimeField()
#     patient = models.ForeignKey('core.Patient')
#     doctor = models.ForeignKey('core.Doctor')
#
#     class Meta:
#         db_table = 'appointment'


class Treatment(AbstractModel):
    start_date = models.DateField()
    finish_date = models.DateField()
    summary = models.CharField(max_length=255)
    info = models.TextField(blank=True, null=True)
    patient = models.ForeignKey('core.Patient', on_delete=models.CASCADE)

    class Meta:
        db_table = 'treatment'
        verbose_name = _('Treatment')
        verbose_name_plural = _('Treatments')


class Medication(AbstractModel):
    summary = models.CharField(max_length=255)
    info = models.TextField(blank=True, null=True)
    drugs = ArrayField(models.CharField(max_length=100))
    medication_date = models.DateField()
    patient = models.ForeignKey('core.Patient', on_delete=models.CASCADE)

    class Meta:
        db_table = 'medication'
        verbose_name = _('Medication')
        verbose_name_plural = _('Medications')


class Diagnosis(AbstractModel):
    diagnosis = models.TextField()
    diagnosis_date = models.DateField()
    patient = models.ForeignKey('core.Patient', on_delete=models.CASCADE)

    class Meta:
        db_table = 'diagnosis'
        verbose_name = _('Diagnosis')
        verbose_name_plural = _('Diagnosis')
