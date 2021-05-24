from django import forms
from .models import SubscribedUser
import re

def getTextInputSetting():
    return forms.TextInput(attrs={'class': 'vertical-form-group__text'})

class SubscribedUserForm(forms.ModelForm):

    class Meta:
        model = SubscribedUser
        fields = ['name', 'mail_address']

    name = forms.CharField(required=True, max_length=256, widget=getTextInputSetting())
    mail_address = forms.EmailField(required=True, max_length=256, widget=getTextInputSetting())
