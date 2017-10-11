from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.core.forms import CustomUserChangeForm, CustomUserCreationForm, RealIndInline, IntIndInline, TextIndInline
from apps.core.models import *
from django.utils.translation import ugettext_lazy as _


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'surname')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    ordering = ('email', 'name', 'surname')
    list_display = ('email', 'name', 'surname', 'is_staff')
    search_fields = ('email', 'name', 'surname')


@admin.register(MedArea)
class MedAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'description')
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(MedTest)
class MedTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'description', '_view_med_area')
    ordering = ('name',)
    search_fields = ('name',)
    inlines = (RealIndInline, IntIndInline, TextIndInline)

    def _view_med_area(self, med_test):
        return med_test.med_area

    _view_med_area.short_description = _('Med Area')


@admin.register(RealInd)
class RealIndAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'description', 'min_norm', 'max_norm')
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(IntInd)
class IntIndAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'description', 'min_norm', 'max_norm')
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(TextInd)
class TextIndAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'description', '_view_values', '_view_med_test')
    ordering = ('name',)
    search_fields = ('name',)
    list_filter = ('med_test__name',)

    def _view_values(self, ind):
        return ', '.join(ind.values)

    def _view_med_test(self, ind):
        return ind.med_test.name

    _view_values.short_description = _('Values')
    _view_med_test.short_description = _('Medical Test')


@admin.register(TestRec)
class TestRecAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'info', 'test_date', '_view_patient')
    ordering = ('test_date',)
    list_filter = ('name',)

    def _view_patient(self, rec):
        return str(rec.patient)

    _view_patient.short_description = _('Patient')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'age', 'gender')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_date', 'info', 'status', '_view_patient')
    ordering = ('appointment_date',)
    list_filter = ('status',)

    def _view_patient(self, appointment):
        return str(appointment.patient)

    _view_patient.short_description = _('Patient')
