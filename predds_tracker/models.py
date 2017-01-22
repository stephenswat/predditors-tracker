from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property
from social_django.utils import load_strategy
from datetime import datetime, timedelta
from eve_sde.models import SolarSystem
import requests

class Character(AbstractUser):
    """
    A database model which is used by the EVE Online SSO to create, store and
    check logins. Stores information from the EVE API such as the character ID.
    """

    latest = models.ForeignKey('LocationRecord', related_name='+', null=True)

    @property
    def ship_location(self):
        res = self.location.copy()
        res.update(self.ship_type)
        res['online'] = self.online
        return res

    @property
    def online(self):
        res = requests.get('https://crest-tq.eveonline.com/characters/%d/location/' % self.character_id,
            headers={'Authorization': 'Bearer ' + self.access_token})
        return res.status_code == 200 and len(res.json()) > 0

    @property
    def location(self):
        res = requests.get('https://esi.tech.ccp.is/latest/characters/%d/location/' % self.character_id,
            headers={'Authorization': 'Bearer ' + self.access_token})
        return res.json()

    @property
    def ship_type(self):
        res = requests.get('https://esi.tech.ccp.is/latest/characters/%d/ship/' % self.character_id,
            headers={'Authorization': 'Bearer ' + self.access_token})
        return res.json()

    @property
    def character_id(self):
        """
        Returns the EVE ID of the character.
        """

        return self.__crest['id']

    @property
    def access_token(self):
        """
        Returns the access token which can be used for CREST calls.
        """

        return self.__crest['access_token']

    @cached_property
    def __crest(self):
        """
        Helper function to occasionally refresh the access token whenever it
        expires.
        """

        provider = self.social_auth.get(provider='eveonline')

        difference = (datetime.strptime(
            provider.extra_data['expires'],
            "%Y-%m-%dT%H:%M:%S"
        ) - datetime.now()).total_seconds()

        if difference < 10:
            provider.refresh_token(load_strategy())
            expiry = datetime.now() + timedelta(seconds=1200)
            provider.extra_data['expires'] = expiry.strftime("%Y-%m-%dT%H:%M:%S")
            provider.save()

        return provider.extra_data

class LocationRecord(models.Model):
    character = models.ForeignKey(Character, db_index=True)
    system = models.ForeignKey(SolarSystem, db_index=True)
    time = models.DateTimeField(auto_now_add=True, db_index=True)
    online = models.BooleanField()
    station_id = models.BigIntegerField(null=True)
    ship_id = models.BigIntegerField()
    ship_type_id = models.BigIntegerField()
