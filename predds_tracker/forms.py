from django.forms import ModelForm
from predds_tracker.models import Character

class CharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = ['track']
