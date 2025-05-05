from django.core.management import call_command
from django.core.management.base import BaseCommand

from suppliers.models import Contact, NetworkNode, Product


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        NetworkNode.objects.all().delete()
        Contact.objects.all().delete()
        Product.objects.all().delete()

        call_command('loaddata', 'suppliers_fixture.json')
        self.stdout.write('Данные из фикстуры Suppliers успешно загружены')
