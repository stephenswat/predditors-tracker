from django import template
from colour import Color

register = template.Library()

@register.filter(name='npc_kill_colour')
def npc_kill_colour(value):
    if value is None or type(value) == str:
        return "#FFFFFF"
    kills = value

    if kills <= 1000:
        gradient = list(Color('white').range_to(Color('#BFFF00'), 11))
        return gradient[(kills + 99) // 100]
    else:
        gradient = list(Color('#BFFF00').range_to(Color('red'), 31))
        return gradient[min(kills + 99 - 1000, 2000) // 100]
