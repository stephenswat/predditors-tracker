from django_cron import CronJobBase, Schedule
from predds_tracker.models import Alt, LocationRecord, Character, SystemStatistic, CHARACTER_INFO_URL
from xml.etree import ElementTree
from django.db import transaction
from datetime import datetime
from collections import defaultdict
from eve_sde.models import SolarSystem
from requests_futures.sessions import FuturesSession
import requests


class UpdateLocations(CronJobBase):
    schedule = Schedule(run_every_mins=5)
    code = 'predds_tracker.update_locations'

    def do(self):
        print("Updating locations...")

        solar_systems = {x['id'] for x in SolarSystem.objects.values('id').all()}
        session = FuturesSession(max_workers=20)
        results = {c: (
            session.get(c.get_location_url(), headers=c.get_headers()),
            session.get(c.get_ship_type_url(), headers=c.get_headers()),
            session.get(c.get_online_url(), headers=c.get_headers()),
        ) for c in Alt.objects.filter(track=True)}

        with transaction.atomic():
            for c, (l, s, o) in results.items():
                print(c, "...")

                try:
                    online = o.result()
                    res = {**l.result().json(), **s.result().json(), 'online': online.status_code == 200 and len(online.json()) > 0}

                    station_id = None

                    if 'station_id' in res:
                        station_id = res['station_id']
                    elif 'structure_id' in res:
                        station_id = res['structure_id']

                    if res['solar_system_id'] not in solar_systems:
                        print("What? %s had a weird system %d!" % (c.name, res['solar_system_id']))
                        continue

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
    schedule = Schedule(run_every_mins=60)
    code = 'predds_tracker.update_alliances'

    def do(self):
        print("Updating alliances...")

        session = FuturesSession(max_workers=20)
        results = {c: session.get(c.update_data_url()) for c in Character.objects.filter()}

        with transaction.atomic():
            for c, d in results.items():
                try:
                    print(c)
                    c.update_data(request=d.result())
                except Exception as e:
                    print(e)


class UpdateStatistics(CronJobBase):
    schedule = Schedule(run_every_mins=60)
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
