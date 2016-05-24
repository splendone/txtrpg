from django.core.management.base import BaseCommand
from taxidata import genData

class Command(BaseCommand):
    args = ''
    help = ''
    def handle(self, *args, **options):
        """docstring for handle"""
        genData.randomData()
    pass