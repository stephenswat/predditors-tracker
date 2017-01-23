import requests
from xml.etree import ElementTree
from predds_tracker.models import SystemStatistic
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.get('https://api.eveonline.com/map/kills.xml.aspx')
        rowset = ElementTree.fromstring(response.content).find('result').find('rowset')
        time = datetime.now()

        with transaction.atomic():
            for row in rowset:
                SystemStatistic(
                    time=time,
                    system_id=int(row.attrib['solarSystemID']),
                    ship_kills=int(row.attrib['shipKills']),
                    pod_kills=int(row.attrib['podKills']),
                    npc_kills=int(row.attrib['factionKills']),
                ).save()
