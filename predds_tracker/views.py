from predds_tracker.models import LocationRecord, Alt, Character, SystemMetadata
from predds_tracker.forms import DeleteAccountForm, AltSetForm, ProfileSettingsForm
from system_statistics.models import SystemStatistic
from eve_sde.models import Region, SolarSystem

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.db.models import Max, F, Count
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
    if request.method == 'POST':
        form = AltSetForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    return render(
        request, 'predds_tracker/profile.html',
        context={'form': DeleteAccountForm(), 'altform': AltSetForm(instance=request.user),
                 'profile_form': ProfileSettingsForm(instance=request.user)}
    )


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

        return redirect('/profile')

@login_required
@user_passes_test(Character.alliance_valid, login_url='/logout/')
def log(request):
    return render(
        request, 'predds_tracker/log.html',
        context={'items': LocationRecord.objects.select_related('ship_type', 'system', 'character').filter(character__main=request.user).order_by('-time')[:200]}
    )


@login_required
@user_passes_test(Character.alliance_valid, login_url='/logout/')
def alts(request):
    prefetch = ['alts', 'alts__latest__system', 'alts__latest__system__constellation', 'alts__latest__system__constellation__region', 'alts__latest__ship_type']

    if request.user.has_perm('predds_tracker.view_all_alts'):
        res = Character.objects.prefetch_related(*prefetch).all()
    else:
        res = Character.objects.prefetch_related(*prefetch).filter(id=request.user.id).all()

    return render(
        request, 'predds_tracker/alts.html',
        context={'mains': res}
    )


@login_required
@user_passes_test(Character.alliance_valid, login_url='/logout/')
def map(request, region_id):
    campers = Alt.objects.select_related('latest__system').filter(latest__system__constellation__region__id=region_id, latest__online=True)
    latest = SystemStatistic.objects.aggregate(Max('time'))['time__max']
    systems = SolarSystem.objects.select_related('data').filter(constellation__region__id=region_id).filter(statistics__time=latest).annotate(npc_kills=F('statistics__npc_kills'))

    count = defaultdict(bool)
    names = set()

    for x in campers:
        names.add(x.latest.system.name)
        count[x.latest.system.id] = True

    return render(
        request, 'predds_tracker/maps/%d.svg' % int(region_id),
        context={
            'region': get_object_or_404(Region, id=region_id),
            'camped': dict(count),
            'systems': {x.id: x for x in systems},
            'dotlan': ','.join(names),
            'coverage': 100*len(names) / systems.count()
        }
    )


@login_required
@user_passes_test(Character.alliance_valid, login_url='/logout/')
def leaderboard(request):
    data = [
        {'name': x['character__main__name'], 'years': x['hours'] // 8760, 'days': (x['hours'] % 8760) // 24, 'hours': x['hours'] % 24, 'total_hours': x['hours']}
        for x in LocationRecord.objects.filter(online=True).values('character__main__name').annotate(hours=(5.0*Count('online'))/60).order_by('-hours')[:25]
    ]

    return render(
        request, 'predds_tracker/leaderboard.html',
        context={
            'data': data
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
