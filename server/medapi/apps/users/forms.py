from django.contrib.auth import get_user_model, logout, login
from django.forms import *

User = get_user_model()


class SignUpForm(Form):
    name = CharField(max_length=50)
    surname = CharField(max_length=50)
    email = CharField(max_length=50)
    password = CharField(max_length=16)
    confirm_password = CharField(max_length=16)

    def is_valid(self):
        valid = super(SignUpForm, self).is_valid()
        if not valid:
            return False
        user = None
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            pass
        if user is not None:
            self._errors['not_unique_email'] = 'User with email "%s" exists' % self.cleaned_data['email']
            return False
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self._errors['not_confirmed_password'] = 'Password is not confirmed'
            return False
        return True

    def create_account(self):
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        surname = self.cleaned_data['surname']
        password = self.cleaned_data['password']
        user = User.objects.create_user(email=email, password=password, name=name, surname=surname)
        user.first_name = name
        user.last_name = surname
        user.save()


class UpdateUserForm(Form):
    name = CharField(max_length=50)
    surname = CharField(max_length=50)

    def __init__(self, request):
        super().__init__(data=request.POST)
        self.user = request.user

    def update(self):
        name = self.cleaned_data['name']
        surname = self.cleaned_data['surname']
        self.user.name = name
        self.user.surname = surname
        self.user.save()


class ChangePasswordForm(Form):
    current_password = CharField(max_length=16)
    new_password = CharField(max_length=16)
    confirm_new_password = CharField(max_length=16)

    def __init__(self, data, user):
        super().__init__(data)
        self.user = user

    def is_valid(self):
        valid = super(ChangePasswordForm, self).is_valid()
        current_password = self.cleaned_data['current_password']
        if not valid:
            return False
        if not self.user.check_password(current_password):
            return False
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']
        if new_password != confirm_new_password:
            return False
        return True

    def change_password(self, request):
        self.user.set_password(self.cleaned_data['new_password'])
        self.user.save()
        logout(request=request)
        login(request=request, user=self.user)
