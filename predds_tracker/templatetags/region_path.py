from django import template
from eve_sde.models import Region

register = template.Library()

@register.filter('region_path')
def region_path(Region):
    return Region.name.replace(' ', '_')
