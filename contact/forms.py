from django import forms
from django.db.models import fields
from .models import Contact

def getTextInputSetting():
    return forms.TextInput(attrs={'class': 'vertical-form-group__text'})

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'mail_address', 'content']
    
    name = forms.CharField(required=True, max_length=256, widget=getTextInputSetting())
    mail_address = forms.EmailField(required=True, max_length=256, widget=getTextInputSetting())
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'vertical-form-group__textarea'}))
