from django.contrib import admin
from predds_tracker.models import Character, LocationRecord, Alt, SystemMetadata


class LocationRecordAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'

    list_display = (
        'character',
        'system',
        'online',
        'station_id',
        'ship_id',
        'ship_type_id',
        'time'
    )


class AltAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'name',
            'id',
            'corporation_id',
            'alliance_id'
        )}),
        ('Tracker', {'fields': (
            'main',
            'track'
        )})
    )

    readonly_fields = (
        'id',
        'name',
        'corporation_id',
        'alliance_id',
        'data'
    )

    list_display = (
        'id',
        'name',
        'main',
        'track'
    )


class SystemMetadataAdmin(admin.ModelAdmin):
    list_display = (
        'system',
        'important'
    )


class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'id',
            'name',
            'corporation_id',
            'alliance_id',
            'last_login'
        )}),
        ('Permissions', {'fields': (
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
    )

    list_display = (
        'id',
        'name',
        'is_staff'
    )

    list_filter = (
        'is_staff',
        'groups'
    )

    readonly_fields = (
        'id',
        'name',
        'corporation_id',
        'alliance_id',
        'data',
        'last_login'
    )

    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )


admin.site.register(Character, UserAdmin)
admin.site.register(LocationRecord, LocationRecordAdmin)
admin.site.register(Alt, AltAdmin)
admin.site.register(SystemMetadata, SystemMetadataAdmin)
