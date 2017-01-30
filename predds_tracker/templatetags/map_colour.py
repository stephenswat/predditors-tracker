from django import template
from colour import Color

register = template.Library()


@register.filter(name='npc_kill_colour')
def npc_kill_colour(value):

    colors = [
        Color('white'),
        Color('#54C45E'),
        Color('#76A654'),
        Color('#98884A'),
        Color('#BA6B41'),
        Color('#DC4D37'),
    ]

    if value is None or type(value) == str:
        return colors[0]
    kills = value

    if kills < 5:
        return colors[0]
    elif kills <= 1000:
        return colors[(kills + 199) // 200]
    else:
        return colors[-1]
