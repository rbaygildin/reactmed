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
    list_display = ('view_name', 'description')
    ordering = ('view_name', )
    search_fields = ('view_name', )


@admin.register(MedTest)
class MedTestAdmin(admin.ModelAdmin):
    list_display = ('view_name', 'description', '_view_med_area')
    ordering = ('view_name', )
    search_fields = ('view_name', )
    inlines = (RealIndInline, IntIndInline, TextIndInline)

    def _view_med_area(self, med_test):
        return med_test.med_area

    _view_med_area.short_description = _('Med Area')


@admin.register(RealInd)
class RealIndAdmin(admin.ModelAdmin):
    list_display = ('view_name', 'description', 'min_norm', 'max_norm')
    ordering = ('view_name',)
    search_fields = ('view_name',)


@admin.register(IntInd)
class IntIndAdmin(admin.ModelAdmin):
    list_display = ('view_name', 'description', 'min_norm', 'max_norm')
    ordering = ('view_name',)
    search_fields = ('view_name',)


@admin.register(TextInd)
class TextIndAdmin(admin.ModelAdmin):
    list_display = ('view_name', 'description', '_view_values', '_view_med_test')
    ordering = ('view_name',)
    search_fields = ('view_name',)
    list_filter = ('med_test__view_name', )

    def _view_values(self, ind):
        return ', '.join(ind.values)

    def _view_med_test(self, ind):
        return ind.med_test.view_name

    _view_values.short_description = _('Values')
    _view_med_test.short_description = _('Medical Test')


@admin.register(TestRec)
class TestRecAdmin(admin.ModelAdmin):
    pass


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass
