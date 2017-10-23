from django.contrib.admin import TabularInline
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from apps.core.models import User, IntInd, RealInd, TextInd


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('email',)


class RealIndInline(TabularInline):
    model = RealInd
    extra = 0


class IntIndInline(TabularInline):
    model = IntInd
    extra = 0


class TextIndInline(TabularInline):
    model = TextInd
    extra = 0
