from predds_tracker.models import Alt

def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    return {
        'is_new': True,
        'user': strategy.create_user(username=kwargs['username'], id=kwargs['response']['CharacterID'])
    }
