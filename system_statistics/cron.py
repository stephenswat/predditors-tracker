from django_cron import CronJobBase, Schedule
from system_statistics.models import SystemStatistic
from predds_tracker.models import SolarSystem
from django.db import transaction

import requests
from collections import defaultdict
from datetime import datetime

class UpdateStatistics(CronJobBase):
    schedule = Schedule(run_every_mins=10)
    code = 'system_statistics.update_statistics'

    def do(self):
        print("Updating statistics...")
        kills = requests.get('https://esi.tech.ccp.is/latest/universe/system_kills/').json()
        jumps = requests.get('https://esi.tech.ccp.is/latest/universe/system_jumps/').json()
        time = datetime.now()
        systems = SolarSystem.objects.values_list('id')

        data = defaultdict(dict)

        for p in kills:
            data[p['system_id']]['ship_kills'] = p['ship_kills']
            data[p['system_id']]['pod_kills'] = p['pod_kills']
            data[p['system_id']]['npc_kills'] = p['npc_kills']

        for p in jumps:
            data[p['system_id']]['ship_jumps'] = p['ship_jumps']

        with transaction.atomic():
            for ssid, stats in data.items():
                SystemStatistic(
                    time=time,
                    system_id=ssid,
                    ship_kills=stats.get('ship_kills', 0),
                    pod_kills=stats.get('pod_kills', 0),
                    npc_kills=stats.get('npc_kills', 0),
                    ship_jumps=stats.get('ship_jumps', 0)
                ).save()
