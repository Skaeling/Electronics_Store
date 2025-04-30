from django.core.management import call_command
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User.objects.all().delete()

        call_command('loaddata', 'users_fixture.json')
        self.stdout.write('Данные из фикстуры Users успешно загружены')
