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
    url(r'^alts/$', views.all_alts, name='alts'),
    url(r'^profile/delete/$', views.delete_account, name='delete_account'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^region/(?P<region>[0-9]+)/', include(regionpatterns)),
    url(r'^help/', views.help, name='help'),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^login/warning/', views.login_warning, name='login_warning'),
    url(r'^', include('social_django.urls', namespace='social')),
    url(r'^$', views.home),
]
