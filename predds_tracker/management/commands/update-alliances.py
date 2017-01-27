from predds_tracker.models import Character
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        for c in Character.objects.filter():
            try:
                print(c)
                c.update_data()
            except Exception as e:
                print(e)
