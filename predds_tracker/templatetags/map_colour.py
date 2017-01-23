from django import template
from colour import Color

register = template.Library()

@register.filter(name='npc_kill_colour')
def npc_kill_colour(value):
    if type(value) == str:
        return "#FFFFFF"
    kills = value

    if kills <= 1000:
        gradient = list(Color('white').range_to(Color('#BFFF00'), 10))
        return gradient[kills // 100]
    else:
        gradient = list(Color('#BFFF00').range_to(Color('red'), 30))
        return gradient[min(kills - 1000, 2000) // 100]
