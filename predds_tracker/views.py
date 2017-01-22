from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from predds_tracker.models import LocationRecord, Character
from eve_sde.models import Region
from collections import defaultdict

def home(request):
    return render(
        request, 'predds_tracker/home.html',
        context={'regions': sorted(list(Region.objects.all()), key=lambda x: x.name)}
    )

def log(request):
    return render(
        request, 'predds_tracker/log.html',
        context={'items': LocationRecord.objects.filter(character=request.user).order_by('-time')[:200]}
    )

def map(request, region):
    return render(
        request, 'predds_tracker/map.html',
        context={
            'region': get_object_or_404(Region, id=region),
            'region': get_object_or_404(Region, id=region)
        },
    )

def map_svg(request, region):
    campers = Character.objects.filter(latest__system__constellation__region__id=region, latest__online=True)

    count = defaultdict(bool)

    for x in campers:
        count[int(x.latest.system.id)] = True

    print(count)

    return render(
        request, 'predds_tracker/maps/%d.svg' % int(region),
        context={'region': get_object_or_404(Region, id=region), 'camped': dict(count)},
        content_type="image/svg+xml"
    )
