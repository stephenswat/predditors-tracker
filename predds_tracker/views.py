from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from predds_tracker.models import LocationRecord, Character
from predds_tracker.forms import CharacterForm
from eve_sde.models import Region
from collections import defaultdict

def home(request):
    return render(
        request, 'predds_tracker/home.html',
        context={'regions': sorted(list(Region.objects.filter(id__lt=11000000)), key=lambda x: x.name)}
    )


@login_required
def profile(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    return render(
        request, 'predds_tracker/profile.html',
        context={'form': CharacterForm(instance=request.user)}
    )


@login_required
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


def help(request):
    return render(request, 'predds_tracker/help.html')


def map_svg(request, region):
    campers = Character.objects.filter(latest__system__constellation__region__id=region, latest__online=True)

    count = defaultdict(bool)

    for x in campers:
        count[int(x.latest.system.id)] = True

    return render(
        request, 'predds_tracker/maps/%d.svg' % int(region),
        context={'region': get_object_or_404(Region, id=region), 'camped': dict(count)},
        content_type="image/svg+xml"
    )
