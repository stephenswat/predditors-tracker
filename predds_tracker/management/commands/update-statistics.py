import requests
from xml.etree import ElementTree
from predds_tracker.models import SystemStatistic
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from datetime import datetime
from collections import defaultdict
from eve_sde.models import SolarSystem

class Command(BaseCommand):
    def handle(self, *args, **options):
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
