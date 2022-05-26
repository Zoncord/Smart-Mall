from django import forms
from malls.models import Mall, Area, Rent
from users.models import BasicCustomer
from django.utils import timezone


class MallForm(forms.ModelForm):
    name = forms.CharField(label='Название', max_length=50, help_text='Максимум 50 символов',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Адрес', max_length=150, help_text='Максимум 150 символов',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    owner = forms.ModelChoiceField(label='Скрыто', queryset=BasicCustomer.objects.all(), empty_label=None, blank=True,
                                   widget=forms.HiddenInput())

    class Meta:
        model = Mall
        fields = ['name', 'description', 'address', 'owner']


class AreaForm(forms.ModelForm):
    price = forms.IntegerField(label='Цена', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    available = forms.ChoiceField(label='Доступность', choices=Area.AVAILABLE_CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    square = forms.IntegerField(label='Площадь в кв. метрах', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    mall = forms.ModelChoiceField(label='Скрыто', queryset=Mall.objects.all(), empty_label=None, blank=True,
                                  widget=forms.HiddenInput())

    class Meta:
        model = Area
        fields = ['price', 'available', 'square', 'mall']


class RentForm(forms.ModelForm):
    rental_start_date_time = forms.DateTimeField(label='Дата и время начала аренды', initial=timezone.now,
                                                 widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    balance = forms.IntegerField(label='Баланс', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(label='Статус аренды', choices=Rent.STATUS_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    area = forms.ModelChoiceField(label='Скрыто', queryset=Area.objects.all(), empty_label=None, blank=True,
                                  widget=forms.HiddenInput())
    tenant = forms.ModelChoiceField(label='Скрыто', queryset=BasicCustomer.objects.all(), empty_label=None, blank=True,
                                    widget=forms.HiddenInput())

    class Meta:
        model = Rent
        fields = ['rental_start_date_time', 'balance', 'status', 'area', 'tenant']


class FiltersForm(forms.Form):
    max_square = forms.CharField(label='Максимальная площадь(необязательно)',
                                 widget=forms.TextInput(attrs={'type': 'number'}), required=False)
    min_square = forms.CharField(label='Минимальная площадь(необязательно)',
                                 widget=forms.TextInput(attrs={'type': 'number'}), required=False)
    max_price = forms.CharField(label='Максимальная цена(необязательно)',
                                widget=forms.TextInput(attrs={'type': 'number'}), required=False)
    min_price = forms.CharField(label='Минимальная цена(необязательно)',
                                widget=forms.TextInput(attrs={'type': 'number'}), required=False)


class Search(FiltersForm):
    search = forms.CharField(label='Поиск', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    owner = forms.CharField(label='Имя владельца(необязательно)', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    field_order = ['search', 'owner', 'max_square', 'min_square', 'max_price', 'min_price']
