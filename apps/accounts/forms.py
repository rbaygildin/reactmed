from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.forms import *


class SignUpForm(Form):
    name = CharField(max_length=50)
    surname = CharField(max_length=50)
    username = CharField(max_length=50)
    password = CharField(max_length=16)
    confirm_password = CharField(max_length=16)

    def is_valid(self):
        valid = super(SignUpForm, self).is_valid()
        if not valid:
            return False
        user = None
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            pass
        if user is not None:
            self._errors['not_unique_username'] = 'User with name "%s" exists' % self.cleaned_data['username']
            return False
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self._errors['not_confirmed_password'] = 'Password is not confirmed'
            return False
        return True

    def create_account(self):
        username = self.cleaned_data['username']
        name = self.cleaned_data['name']
        surname = self.cleaned_data['surname']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username, '', password)
        user.first_name = name
        user.last_name = surname
        user.save()
