from predds_tracker.models import Character
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

@login_required
def warp_bomb(request):
    return render(request, 'tools/warp_time.html')

@login_required
def bomb_damage(request):
    return render(request, 'tools/bomb_damage.html')
