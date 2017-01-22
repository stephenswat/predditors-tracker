from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from predds_tracker import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^log/$', views.log, name='log'),
    url(r'^map/(?P<region>[0-9]+)/$', views.map, name='display_region'),
    url(r'^map/(?P<region>[0-9]+)/svg/', views.map_svg, name='region_svg'),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', views.home),
]
