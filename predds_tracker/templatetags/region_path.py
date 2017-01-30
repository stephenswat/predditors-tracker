from django import template

register = template.Library()


@register.filter('region_path')
def region_path(region):
    return region.name.replace(' ', '_')
