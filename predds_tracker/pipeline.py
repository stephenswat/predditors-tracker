import requests

from django.conf import settings
from social_core.exceptions import AuthForbidden

from predds_tracker.models import Alt


def create_alt(backend, user, response, *args, **kwargs):
    if kwargs['new_association'] and not kwargs['is_new']:
        Alt(
            id=response['CharacterID'],
            name=response['CharacterName'],
            main=user,
            data=kwargs['social']
        ).save()

        return {'is_alt': True}

    return {'is_alt': False}


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        if user.id == kwargs['uid'] and user.name != kwargs['username']:
            user.name = details['username']
            user.save()
        return {'is_new': False}

    user = strategy.create_user(
        username=kwargs['username'],
        id=kwargs['response']['CharacterID']
    )

    user.update_data()

    return {
        'is_new': True,
        'user': user
    }


def reject_alliance(strategy, details, backend, **kwargs):
    if kwargs.get('is_alt', False):
        return

    if settings.VALID_ALLIANCE_IDS is None:
        return

    data = requests.get('https://esi.tech.ccp.is/latest/characters/%d/?datasource=tranquility' % kwargs['user'].id).json()

    if data.get('alliance_id', -1) not in settings.VALID_ALLIANCE_IDS:
        raise AuthForbidden(backend, 'Forbidden alliance ID.')


def get_username(strategy, details, backend, user=None, *args, **kwargs):
    return {'username': details['fullname']}
