from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.db.models import Max
from django.http import HttpResponse
from predds_tracker.models import LocationRecord, Alt, Character, SystemStatistic, SystemMetadata
from predds_tracker.forms import AltForm, DeleteAccountForm
from eve_sde.models import Region, SolarSystem
from collections import defaultdict

def home(request):
    important = set(SystemMetadata.objects.filter(important=True).values_list('system__constellation__region', flat=True).distinct())

    return render(
        request, 'predds_tracker/home.html',
        context={
            'regions': sorted(list(Region.objects.filter(id__lt=11000000)), key=lambda x: x.name),
            'important': important
        }
    )


@login_required
def profile(request):
    return render(
        request, 'predds_tracker/profile.html',
        context={'form': DeleteAccountForm()}
    )


@login_required
@user_passes_test(Character.alliance_valid, login_url='/logout/')
def log(request):
    return render(
        request, 'predds_tracker/log.html',
        context={'items': LocationRecord.objects.filter(character__main=request.user).order_by('-time')[:200]}
    )


@login_required
@user_passes_test(Character.alliance_valid, login_url='/logout/')
@permission_required('predds_tracker.view_all_alts', raise_exception=True)
def all_alts(request):
    return render(
        request, 'predds_tracker/alts.html',
        context={'mains': Character.objects.all()}
    )


@login_required
@user_passes_test(Character.alliance_valid, login_url='/logout/')
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


@login_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid() and form.cleaned_data['delete']:
            request.user.delete()

    return redirect('/')


def help(request):
    return render(request, 'predds_tracker/help.html')


def login_warning(request):
    return render(request, 'predds_tracker/login_warning.html')
