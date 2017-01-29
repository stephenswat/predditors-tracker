from django import forms
from predds_tracker.models import Character, Alt

class AltForm(forms.ModelForm):
    class Meta:
        model = Alt
        fields = ['track']

class DeleteAccountForm(forms.Form):
    delete = forms.BooleanField('Confirmation')
