from .models import CustomerDetails
from django import forms


class ProfileForm(forms.ModelForm):

    class Meta:
        model = CustomerDetails
        exclude = ['services']
        widgets = {
        'email': forms.TextInput(attrs={'readonly': 'readonly','size':'60', 'style': 'border: transparent'}),
        'name': forms.TextInput(attrs={'size': '100'}),
        'phones': forms.TextInput(attrs={'size': '100'}),
        'cpf': forms.TextInput(attrs={'size':'14'}),
        'cnpj': forms.TextInput(attrs={'size': '18'}),
        'country_abbreviation': forms.TextInput(attrs={'size': '2'}),
        'state_abbreviation': forms.TextInput(attrs={'size': '2'}),
        'city': forms.TextInput(attrs={'size': '60'}),
        'full_address': forms.TextInput(attrs={'size': '200'}),
        'responsibles': forms.TextInput(attrs={'size': '200'}),
        }