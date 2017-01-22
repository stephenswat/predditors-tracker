from predds_tracker.models import Character, LocationRecord
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        for c in Character.objects.all():
            print(c, "...")
            try:
                res = c.ship_location
                print(res)

                station_id = None

                if 'station_id' in res:
                    station_id = res['station_id']
                elif 'structure_id' in res:
                    station_id = res['structure_id']

                new_entry = LocationRecord(
                    character = c,
                    online = res['online'],
                    system_id = res['solar_system_id'],
                    station_id = station_id,
                    ship_id = res['ship_item_id'],
                    ship_type_id = res['ship_item_id']
                )

                new_entry.save()
                c.latest = new_entry
                c.save()
            except Exception as e:
                print(e)
