from django.core.management.base import BaseCommand, CommandError
from first_app.models import Cell

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('wr_sz', type=int)

    def handle(self, *args, **options):
        wr_sz = options['wr_sz']
        for x in range(wr_sz):
            for y in range(wr_sz):
                cell = Cell()
                cell.x = x
                cell.y = y
                cell.save()
        print('World of %s cells succesfully generated' % wr_sz**2)
