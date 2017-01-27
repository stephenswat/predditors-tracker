from django import template
from colour import Color

register = template.Library()

noKillsColor=Color('white')
thousandKillsColor=Color('#BFFF00')
maxKillsColor=Color('red')

@register.filter(name='npc_kill_colour')
def npc_kill_colour(value):
    
    if value is None or type(value) == str:
        return noKillsColor
    kills = value

    if kills <= 1000:
        gradient = list(noKillsColor.range_to(thousandKillsColor, 11))
        return gradient[(kills + 99) // 100]
    else:
        gradient = list(thousandKillsColor.range_to(maxKillsColor, 31))
        return gradient[min(kills + 99 - 1000, 3000) // 100]
