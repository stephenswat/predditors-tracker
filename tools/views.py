from django.shortcuts import render

# Create your views here.
def warp_bomb(request):
    return render(request, 'tools/warp_time.html')
