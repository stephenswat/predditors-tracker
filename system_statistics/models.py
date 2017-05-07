from django.db import models

from eve_sde.models import SolarSystem

class SystemStatistic(models.Model):
    system = models.ForeignKey(SolarSystem, related_name='statistics')
    time = models.DateTimeField(db_index=True)
    ship_kills = models.IntegerField()
    pod_kills = models.IntegerField()
    npc_kills = models.IntegerField()
    ship_jumps = models.IntegerField()
