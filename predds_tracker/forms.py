from django.forms import ModelForm
from predds_tracker.models import Character, Alt

class AltForm(ModelForm):
    class Meta:
        model = Alt
        fields = ['track']
