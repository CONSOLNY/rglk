from django.core.management.base import BaseCommand, CommandError
from first_app.models import Cell

class Command(BaseCommand):
    def handle(self, *args, **options):
        Cell.objects.all().delete()
        print('All cells in world succesfully destroyed')
