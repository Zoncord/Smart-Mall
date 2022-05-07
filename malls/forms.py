from django import forms
from malls.models import Mall


class MallForm(forms.ModelForm):
    name = forms.CharField(label='Название', max_length=50, help_text='Максимум 50 символов', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Адрес', max_length=150, help_text='Максимум 150 символов', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Mall
        fields = ['name', 'description', 'address']
