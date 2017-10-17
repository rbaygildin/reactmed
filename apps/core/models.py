# -*- coding: utf-8 -*- 
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import *
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from transliterate import translit
from datetime import date, timedelta
from django.conf import settings

from apps.core.managers import UserManager

GENDER = (
    ('Мужской', 'Мужской'),
    ('Женский', 'Женский')
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

APPOINTMENT_STATUS = (
    ('Назначено', 'Назначено'),
    ('Завершено', 'Завершено'),
    ('Отменено', 'Отменено')
)

USER_ROLES = (
    ('ADMIN', 'ADMIN'),
    ('DOCTOR', 'DOCTOR')
)


class AbstractModel(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(verbose_name=_('Email'), max_length=30, unique=True)
    name = models.CharField(verbose_name=_('Имя'), max_length=30)
    surname = models.CharField(verbose_name=_('Фамилия'), max_length=30)
    patronymic = models.CharField(verbose_name=_('Отчество'), max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(_('Администратор?'), default=False)
    date_joined = models.DateTimeField(default=now())
    role = models.CharField(verbose_name=_('Роль'), max_length=20, choices=USER_ROLES, default='DOCTOR')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

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


class Patient(AbstractModel):
    name = models.CharField(verbose_name=_('Имя'), max_length=50)
    surname = models.CharField(verbose_name=_('Фамилия'), max_length=50)
    patronymic = models.CharField(verbose_name=_('Отчество'), max_length=50, blank=True, null=True)
    gender = models.CharField(verbose_name=_('Пол'), max_length=20, choices=GENDER)
    birthday = models.DateField(verbose_name=_('Дата рождения'))
    blood_group = models.CharField(verbose_name=_('Группа крови'), max_length=20, choices=BLOOD_GROUP, blank=True,
                                   null=True)
    rh_factor = models.CharField(verbose_name=_('Резус-фактор'), max_length=20, choices=RH_FACTOR, blank=True, null=True)
    is_disabled = models.BooleanField(verbose_name=_('Инвалидность'), default=False)
    omi_card = models.CharField(verbose_name=_('ОМС'), max_length=30, blank=True, null=True)
    address = models.CharField(verbose_name=_('Адрес проживания'), max_length=255, blank=True, null=True)
    occupation = models.CharField(verbose_name=_('Род деятельности'), max_length=100, blank=True, null=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='patients', on_delete=models.CASCADE)

    @property
    def age(self):
        return (date.today() - self.birthday) // timedelta(days=365.2425)

    @property
    def short_name(self):
        if self.patronymic is not None and self.patronymic != '':
            return '%s %s %s' % (self.surname, self.name[0], self.patronymic[0])
        else:
            return '%s %s.' % (self.surname, self.name[0])

    @property
    def short_info(self):
        return '%s (ОМС № %s)' % (self.short_name, self.omi_card)

    @property
    def full_name(self):
        if self.patronymic is not None and self.patronymic != '':
            return '%s %s %s' % (self.surname, self.name, self.patronymic)
        else:
            return '%s %s' % (self.surname, self.name)

    class Meta:
        db_table = 'patient'
        verbose_name = _('Пациент')
        verbose_name_plural = _('Пациенты')


class BaseMedType(AbstractModel):
    name = models.CharField(max_length=200, verbose_name=_('Название'))
    short_name = models.CharField(max_length=200, unique=True, blank=True, null=True, verbose_name=_('Идентификатор'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Описание'))

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
        verbose_name = _('Медицинская область')
        verbose_name_plural = _('Медицинские области')


class MedTest(BaseMedType):
    med_area = models.ForeignKey('core.MedArea')

    def save(self, *args, **kwargs):
        if self.short_name is None or self.short_name == '':
            self.short_name = self.med_area.short_name + '_' + translit(self.name, 'ru', reversed=True).lower().replace(' ', '_')
        super(MedTest, self).save(*args, **kwargs)

    class Meta:
        db_table = 'med_test'
        verbose_name = _('Тип обследования')
        verbose_name_plural = _('Типы обследования')


class RealInd(BaseMedType):
    med_test = models.ForeignKey('core.MedTest', related_name='real_inds')
    min_norm = models.FloatField(blank=True, null=True, verbose_name=_('Минимальная норма'))
    max_norm = models.FloatField(blank=True, null=True, verbose_name=_('Максимальная норма'))
    min_critical = models.FloatField(blank=True, null=True, verbose_name=_('Минимальная критическая норма'))
    max_critical = models.FloatField(blank=True, null=True, verbose_name=_('Максимальная критическая норма'))
    unit = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Единица измерения'))

    class Meta:
        db_table = 'real_ind'
        verbose_name = _('Вещественный показатель')
        verbose_name_plural = _('Вещественные показатели')

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
    min_norm = models.IntegerField(blank=True, null=True, verbose_name=_('Минимальная норма'))
    max_norm = models.IntegerField(blank=True, null=True, verbose_name=_('Максимальная норма'))
    min_critical = models.IntegerField(blank=True, null=True, verbose_name=_('Минимальная критическая норма'))
    max_critical = models.IntegerField(blank=True, null=True, verbose_name=_('Максимальная критическая норма'))
    unit = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Единица измерения'))

    class Meta:
        db_table = 'int_ind'
        verbose_name = _('Целый показатель')
        verbose_name_plural = _('Целые показатели')

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
    values = ArrayField(models.CharField(max_length=255), null=True, blank=True, verbose_name=_('Принимаемые значения'))

    class Meta:
        db_table = 'text_ind'
        verbose_name = _('Строковой показатель')
        verbose_name_plural = _('Строковые показатели')

    def save(self, *args, **kwargs):
        if self.short_name is None or self.short_name == '':
            self.short_name = self.med_test.short_name + '_' + translit(self.name, 'ru', reversed=True).lower().replace(' ', '_')
        super(TextInd, self).save(*args, **kwargs)


class TestRec(AbstractModel):
    name = models.CharField(max_length=200, verbose_name=_('Тип обследования'))
    short_name = models.CharField(max_length=200, verbose_name=_('Тип обследования (идентификатор)'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Описание'))
    real_inds = JSONField(blank=True, null=True, verbose_name=_('Вещественные показатели'))
    int_inds = JSONField(blank=True, null=True, verbose_name=_('Целые показатели'))
    text_inds = JSONField(blank=True, null=True, verbose_name=_('Строковые показатели'))
    summary = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Краткая информация'))
    info = models.TextField(blank=True, null=True, verbose_name=_('Информация'))
    test_date = models.DateField(verbose_name=_('Дата проведения'))
    patient = models.ForeignKey('core.Patient', on_delete=models.CASCADE, related_name='test_recs', verbose_name=_('Пациент'))

    class Meta:
        db_table = 'test_rec'
        verbose_name = _('Обследование')
        verbose_name_plural = _('Обследования')


class Attachment(AbstractModel):
    name = models.CharField(max_length=200, verbose_name=_('Название'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Описание'))
    content = models.BinaryField(verbose_name=_('Содержимое'))
    test_record = models.ForeignKey('core.TestRec', verbose_name=_('Обследование'))

    class Meta:
        db_table = 'attachment'
        verbose_name = _('Файл')
        verbose_name_plural = _('Файлы')


class Appointment(AbstractModel):
    appointment_date = models.DateTimeField(verbose_name=_('Дата приема'))
    info = models.TextField(blank=True, null=True, verbose_name=_('Информация'))
    complaints = models.TextField(blank=True, null=True, verbose_name=_('Жалобы пациента'))
    status = models.CharField(max_length=30, choices=APPOINTMENT_STATUS, default='Назначено', verbose_name=_('Статус'))
    patient = models.ForeignKey('core.Patient', related_name='appointments', on_delete=models.CASCADE, verbose_name=_('Пациент'))

    class Meta:
        db_table = 'appointment'
        verbose_name = _('Прием')
        verbose_name_plural = _('Приемы')


class Treatment(AbstractModel):
    start_date = models.DateField(verbose_name=_('Начало лечения'))
    finish_date = models.DateField(verbose_name=_('Конец лечения'))
    summary = models.CharField(max_length=255, verbose_name=_('Краткая информация'))
    info = models.TextField(blank=True, null=True, verbose_name=_('Информация'))
    patient = models.ForeignKey('core.Patient', on_delete=models.CASCADE, verbose_name=_('Пациент'))

    class Meta:
        db_table = 'treatment'
        verbose_name = _('Лечение')
        verbose_name_plural = _('Лечение')


class Medication(AbstractModel):
    summary = models.CharField(max_length=255, verbose_name=_('Краткая информация'))
    info = models.TextField(blank=True, null=True, verbose_name=_('Информация'))
    drugs = ArrayField(models.CharField(max_length=100), verbose_name=_('Лекарства'))
    medication_date = models.DateField(verbose_name=_('Дата медикаментации'))
    patient = models.ForeignKey('core.Patient', on_delete=models.CASCADE, verbose_name=_('Пациент'))

    class Meta:
        db_table = 'medication'
        verbose_name = _('Медикаментация')
        verbose_name_plural = _('Медикаментация')


class Diagnosis(AbstractModel):
    diagnosis = models.TextField(verbose_name=_('Диагноз'))
    diagnosis_date = models.DateField(verbose_name=_('Дата диагноза'))
    patient = models.ForeignKey('core.Patient', on_delete=models.CASCADE, verbose_name=_('Пациент'))

    class Meta:
        db_table = 'diagnosis'
        verbose_name = _('Диагноз')
        verbose_name_plural = _('Диагнозы')
