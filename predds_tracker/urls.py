from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from predds_tracker import views

regionpatterns = [
    url(r'^$', views.map, name='display_region'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^log/$', views.log, name='log'),
    url(r'^alts/$', views.alts, name='alts'),
    url(r'^profile/delete/$', views.delete_account, name='delete_account'),
    url(r'^profile/update_profile/$', views.update_profile, name='update_profile'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^region/(?P<region_id>[0-9]+)/', include(regionpatterns)),
    url(r'^tools/', include('tools.urls')),
    url(r'^help/', views.help, name='help'),
    url(r'^leaderboard/', views.leaderboard, name='leaderboard'),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^login/warning/', views.login_warning, name='login_warning'),
    url(r'^', include('social_django.urls', namespace='social')),
    url(r'^$', views.home),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
