from django.contrib import admin
from predds_tracker.models import Character, LocationRecord, Alt, SystemMetadata

class LocationRecordAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    list_display = ('character', 'system', 'online', 'station_id', 'ship_id', 'ship_type_id', 'time')

class AltAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'main', 'track')

class SystemMetadataAdmin(admin.ModelAdmin):
    list_display = ('system', 'important')

class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    list_display = ('name', 'is_staff')
    list_filter = ('is_staff', 'groups')
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Character, UserAdmin)
admin.site.register(LocationRecord, LocationRecordAdmin)
admin.site.register(Alt, AltAdmin)
admin.site.register(SystemMetadata, SystemMetadataAdmin)
