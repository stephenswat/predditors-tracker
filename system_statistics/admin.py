from django.contrib import admin
from system_statistics.models import SystemStatistic

class SystemStatisticAdmin(admin.ModelAdmin):
    def get_system_name(self, obj):
        return obj.system.name

    get_system_name.short_description = 'System Name'

    fieldsets = (
        (None, {'fields': (
            'time',
            'system'
        )}),
        ('Statistics', {'fields': (
            'ship_kills',
            'pod_kills',
            'npc_kills',
            'ship_jumps'
        )}),
    )

    list_display = (
        'time',
        'get_system_name'
    )

    ordering = (
        'time',
    )

admin.site.register(SystemStatistic, SystemStatisticAdmin)
