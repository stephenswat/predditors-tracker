from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from predds_tracker.models import Character, LocationRecord

class LocationRecordAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    list_display = ('character', 'system', 'online', 'station_id', 'ship_id', 'ship_type_id', 'time')

admin.site.register(Character, UserAdmin)
admin.site.register(LocationRecord, LocationRecordAdmin)
