from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.functional import cached_property
from django.conf import settings
from social_django.utils import load_strategy
from datetime import datetime, timedelta
from eve_sde.models import SolarSystem, ItemType
import xml.etree.ElementTree
import requests

class EveCharacter(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    data = models.OneToOneField('social_django.UserSocialAuth', null=True)
    corporation_id = models.BigIntegerField(null=True)
    alliance_id = models.BigIntegerField(null=True)

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

        difference = (datetime.strptime(
            self.data.extra_data['expires'],
            "%Y-%m-%dT%H:%M:%S"
        ) - datetime.now()).total_seconds()

        if difference < 10:
            try:
                self.data.refresh_token(load_strategy())
                expiry = datetime.now() + timedelta(seconds=1200)
                self.data.extra_data['expires'] = expiry.strftime("%Y-%m-%dT%H:%M:%S")
                self.data.save()
            except requests.exceptions.HTTPError as e:
                print(e)

        return self.data.extra_data

    def alliance_valid(self):
        return self.alliance_id in settings.VALID_ALLIANCE_IDS

    def update_data(self):
        tree = xml.etree.ElementTree.fromstring(requests.get('https://api.eveonline.com/eve/CharacterInfo.xml.aspx?characterID=%d' % self.id).text)[1]

        corporation_tag = tree.find('corporationID')
        if corporation_tag is not None:
            self.corporation_id = int(corporation_tag.text)
        else:
            self.corporation_id = None

        alliance_tag = tree.find('allianceID')
        if alliance_tag is not None:
            self.alliance_id = int(alliance_tag.text)
        else:
            self.alliance_id = None

        self.save()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, name, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(name=name, **extra_fields)
        user.save(using=self._db)
        return user

class Character(EveCharacter, AbstractBaseUser, PermissionsMixin):
    """
    A database model which is used by the EVE Online SSO to create, store and
    check logins. Stores information from the EVE API such as the character ID.
    """

    is_staff = models.BooleanField(
        'Staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    password = None

    USERNAME_FIELD = 'name'

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Alt(EveCharacter):
    main = models.ForeignKey(Character, related_name='alts')
    latest = models.ForeignKey('LocationRecord', related_name='+', null=True)
    track = models.BooleanField(
        'Enable tracking',
        default=True,
        help_text='If disabled, temporarily stop this character from being tracked.'
    )

    @property
    def ship_location(self):
        res = self.location.copy()
        res.update(self.ship_type)
        res['online'] = self.online
        return res

    @property
    def online(self):
        res = requests.get('https://crest-tq.eveonline.com/characters/%d/location/' % self.id,
            headers={'Authorization': 'Bearer ' + self.access_token})
        return res.status_code == 200 and len(res.json()) > 0

    @property
    def location(self):
        res = requests.get('https://esi.tech.ccp.is/latest/characters/%d/location/' % self.id,
            headers={'Authorization': 'Bearer ' + self.access_token})
        return res.json()

    @property
    def ship_type(self):
        res = requests.get('https://esi.tech.ccp.is/latest/characters/%d/ship/' % self.id,
            headers={'Authorization': 'Bearer ' + self.access_token})
        return res.json()

    class Meta:
        permissions = (
            ("view_all_alts", "Can view lists of all alts and their owners."),
        )

class LocationRecord(models.Model):
    character = models.ForeignKey(Alt, db_index=True)
    system = models.ForeignKey(SolarSystem, db_index=True)
    time = models.DateTimeField(auto_now_add=True, db_index=True)
    online = models.BooleanField()
    station_id = models.BigIntegerField(null=True)
    ship_id = models.BigIntegerField()
    ship_type = models.ForeignKey(ItemType)
    ship_name = models.CharField(max_length=128)

class SystemMetadata(models.Model):
    system = models.OneToOneField(SolarSystem, related_name='data')
    important = models.BooleanField()
    note = models.TextField(blank=True)

class SystemStatistic(models.Model):
    system = models.ForeignKey(SolarSystem, related_name='statistics')
    time = models.DateTimeField(db_index=True)
    ship_kills = models.IntegerField()
    pod_kills = models.IntegerField()
    npc_kills = models.IntegerField()
