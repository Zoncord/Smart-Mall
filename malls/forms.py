from django import forms
from malls.models import Mall, Area
from users.models import BasicCustomer


class MallForm(forms.ModelForm):
    name = forms.CharField(label='Название', max_length=50, help_text='Максимум 50 символов', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Адрес', max_length=150, help_text='Максимум 150 символов', widget=forms.TextInput(attrs={'class': 'form-control'}))
    owner = forms.ModelChoiceField(label='Скрыто', queryset=BasicCustomer.objects.all(), empty_label=None, blank=True, widget=forms.HiddenInput())

    class Meta:
        model = Mall
        fields = ['name', 'description', 'address', 'owner']


class AreaForm(forms.ModelForm):
    price = forms.IntegerField(label='Цена', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    available = forms.ChoiceField(label='Доступность', choices=Area.AVAILABLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    square = forms.IntegerField(label='Площадь в кв. метрах', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    mall = forms.ModelChoiceField(label='Скрыто', queryset=Mall.objects.all(), empty_label=None, blank=True, widget=forms.HiddenInput())

    class Meta:
        model = Area
        fields = ['price', 'available', 'square', 'mall']
