from django.core.management import BaseCommand

from apps.core.models import User, Patient


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Clear models')
        User.objects.all().delete()
        Patient.objects.all().delete()
