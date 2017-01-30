from predds_tracker.models import Alt


def create_alt(backend, user, response, *args, **kwargs):
    if kwargs['new_association'] and not kwargs['is_new']:
        Alt(
            id=response['CharacterID'],
            name=response['CharacterName'],
            main=user,
            data=kwargs['social']
        ).save()


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


def get_username(strategy, details, backend, user=None, *args, **kwargs):
    return {'username': details['fullname']}
