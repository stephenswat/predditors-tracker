from predds_tracker.models import Character
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

@login_required
@user_passes_test(Character.alliance_valid, login_url='/logout/')
def warp_bomb(request):
    return render(request, 'tools/warp_time.html')
