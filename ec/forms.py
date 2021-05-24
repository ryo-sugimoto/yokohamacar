from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Order

def getTextInputSetting():
    return forms.TextInput(attrs={'class': 'vertical-form-group__text'})

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['product', 'product_option', 'buyer_name', 'buyer_address', 'buyer_zip_code', 'buyer_tel', 'buyer_email']
        widgets = {
            'product': forms.HiddenInput(),
            'product_option': forms.HiddenInput()
        }
    
    buyer_name = forms.CharField(required=True, label='お名前', max_length=256, widget=getTextInputSetting())
    buyer_address = forms.CharField(required=True, label='住所', max_length=256, widget=getTextInputSetting())
    buyer_zip_code = forms.CharField(required=True, label='郵便番号（ハイフン無し）', max_length=256, widget=getTextInputSetting())
    buyer_tel = forms.CharField(required=True, label='電話番号（ハイフン無し）', max_length=256, widget=getTextInputSetting())
    buyer_email = forms.EmailField(required=True, label='メールアドレス', max_length=256, widget=getTextInputSetting())
