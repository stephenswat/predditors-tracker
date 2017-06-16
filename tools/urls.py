from tools import views
from django.conf.urls import url, include

urlpatterns = [
    url(r'^warp_bomb/', views.warp_bomb, name='warp_bomb'),
]
