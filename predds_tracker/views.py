from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Max
from django.http import HttpResponse
from predds_tracker.models import LocationRecord, Alt, Character, SystemStatistic
from predds_tracker.forms import AltForm
from eve_sde.models import Region, SolarSystem
from collections import defaultdict

def home(request):
    return render(
        request, 'predds_tracker/home.html',
        context={'regions': sorted(list(Region.objects.filter(id__lt=11000000)), key=lambda x: x.name)}
    )


@login_required
def profile(request):
    if request.method == 'POST':
        form = AltForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    return render(
        request, 'predds_tracker/profile.html',
        context={'form': AltForm(instance=request.user)}
    )


@login_required
def log(request):
    return render(
        request, 'predds_tracker/log.html',
        context={'items': LocationRecord.objects.filter(character__main=request.user).order_by('-time')[:200]}
    )


@login_required
@permission_required('predds_tracker.view_all_alts', raise_exception=True)
def all_alts(request):
    return render(
        request, 'predds_tracker/alts.html',
        context={'mains': Character.objects.all()}
    )


def map(request, region):
    campers = Alt.objects.filter(latest__system__constellation__region__id=region, latest__online=True)
    latest = SystemStatistic.objects.aggregate(Max('time'))['time__max']
    systems = SolarSystem.objects.filter(constellation__region__id=region, statistics__time=latest).values_list('id', 'statistics__npc_kills')

    count = defaultdict(bool)
    names = set()

    for x in campers:
        names.add(x.latest.system.name)
        count[x.latest.system.id] = True

    print(','.join(names))

    return render(
        request, 'predds_tracker/maps/%d.svg' % int(region),
        context={
            'region': get_object_or_404(Region, id=region),
            'camped': dict(count),
            'npc_kills': {x[0]: x[1] for x in systems},
            'dotlan': ','.join(names)
        }
    )


def help(request):
    return render(request, 'predds_tracker/help.html')
