from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from mimesis import Personal, Address

from apps.core.models import Patient

User = get_user_model()

ru = Personal('ru')
ad = Address('ru')


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _populate_doctors(self):
        for i in range(30):
            name = ru.name(gender='male')
            surname = ru.surname(gender='male')
            email = ru.email()
            password = 'doctor95root'
            user = User.objects.create_user(email=email, password=password, name=name, surname=surname)
            user.save()

    def _set_patient_address(self):
        for p in Patient.objects.all():
            p.address = 'Москва, ' + ad.address()
            p.save()

    def handle(self, *args, **options):
        self._set_patient_address()
