from django_cron import CronJobBase, Schedule
from predds_tracker.models import Alt, LocationRecord, Character
from xml.etree import ElementTree
from predds_tracker.models import SystemStatistic
from django.db import transaction
from datetime import datetime
from collections import defaultdict
from eve_sde.models import SolarSystem
import requests


class UpdateLocations(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'predds_tracker.update_locations'

    def do(self):
        print("Updating locations...")
        for c in Alt.objects.filter(track=True):
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
                    character=c,
                    online=res['online'],
                    system_id=res['solar_system_id'],
                    station_id=station_id,
                    ship_id=res['ship_item_id'],
                    ship_type_id=res['ship_type_id'],
                    ship_name=res['ship_name']
                )

                new_entry.save()
                c.latest = new_entry
                c.save()
            except Exception as e:
                print(e)


class UpdateAlliances(CronJobBase):
    RUN_EVERY_MINS = 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'predds_tracker.update_alliances'

    def do(self):
        print("Updating alliances...")
        for c in Character.objects.filter():
            try:
                print(c)
                c.update_data()
            except Exception as e:
                print(e)


class UpdateStatistics(CronJobBase):
    RUN_EVERY_MINS = 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'predds_tracker.update_statistics'

    def do(self):
        print("Updating statistics...")
        response = requests.get('https://api.eveonline.com/map/kills.xml.aspx')
        rowset = ElementTree.fromstring(response.content).find('result').find('rowset')
        time = datetime.now()

        ship_kills = defaultdict(int)
        pod_kills = defaultdict(int)
        npc_kills = defaultdict(int)

        for row in rowset:
            ssid = int(row.attrib['solarSystemID'])
            ship_kills[ssid] = int(row.attrib['shipKills'])
            pod_kills[ssid] = int(row.attrib['podKills'])
            npc_kills[ssid] = int(row.attrib['factionKills'])

        with transaction.atomic():
            for ssid in SolarSystem.objects.values_list('id'):
                ssid = ssid[0]
                SystemStatistic(
                    time=time,
                    system_id=ssid,
                    ship_kills=ship_kills[ssid],
                    pod_kills=pod_kills[ssid],
                    npc_kills=npc_kills[ssid],
                ).save()
