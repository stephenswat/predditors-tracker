from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from predds_tracker.models import Alt

def single_association(backend, user, response, *args, **kwargs):
    if kwargs['new_association'] and not kwargs['is_new']:
        Alt(main=user, data=kwargs['social']).save()
