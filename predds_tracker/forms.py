from django import forms


class DeleteAccountForm(forms.Form):
    delete = forms.BooleanField('Confirmation')
