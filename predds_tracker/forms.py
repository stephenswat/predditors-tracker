from django import forms
from predds_tracker.models import Character, Alt


class AltInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        for x in self.forms:
            if x.instance not in self.instance.alts.all():
                raise forms.ValidationError('Trying to alter an alt not owned by the user.')


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['map_auto_update']


class AltForm(forms.ModelForm):
    class Meta:
        model = Alt
        fields = ['track']


class DeleteAccountForm(forms.Form):
    delete = forms.BooleanField('Confirmation')


AltSetForm = forms.inlineformset_factory(
    Character,
    Alt,
    extra=0,
    form=AltForm,
    formset=AltInlineFormSet,
    can_delete=False
)
