from django import template

register = template.Library()

def security_background_colour(value):
    if value >= 1.0:
        return "#2FEFEF"
    elif value >= 0.9:
        return "#48F0C0"
    elif value >= 0.8:
        return "#00EF47"
    elif value >= 0.7:
        return "#00F000"
    elif value >= 0.6:
        return "#8FEF2F"
    elif value >= 0.5:
        return "#EFEF00"
    elif value >= 0.4:
        return "#D77700"
    elif value >= 0.3:
        return "#F06000"
    elif value >= 0.2:
        return "#F04800"
    elif value >= 0.1:
        return "#D73000"
    else:
        return "#F00000"

def security_text_colour(value):
    if value >= 0.5:
        return "#000000"
    else:
        return "#FFFFFF"

register.filter('security_background_colour', security_background_colour)
register.filter('security_text_colour', security_text_colour)
