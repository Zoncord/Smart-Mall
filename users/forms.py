import imp
from django import forms
from django.contrib.auth.forms import (
    PasswordChangeForm,
    SetPasswordForm,
    PasswordResetForm,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation


class ImageWidget(forms.widgets.ClearableFileInput):
    template_name = 'widgets/image.html'


class BeautifulAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email', 'class': 'form-control'}
        ),
    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'class': 'form-control'}
        ),
    )


class UserForm(forms.ModelForm):
    email = forms.EmailField(
        label='Адрес электронной почты',
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    first_name = forms.CharField(
        label='Имя',
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    middle_name = forms.CharField(
        label='Отчество',
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    mobile_number = forms.CharField(
        label='Номер телефона',
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    is_lessor = forms.BooleanField(help_text="Выбрать этот пункт если хотите стать арендодателем", required=False, label='Арендодатель')
    is_tenant = forms.BooleanField(help_text="Выбрать этот пункт если хотите стать арендатором", required=False, label='Арендатор')
    avatar = forms.ImageField(label='Аватар', required=False, widget=ImageWidget())

    class Meta:
        model = get_user_model()
        fields = (
            'avatar',
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'mobile_number',
            'is_lessor',
            'is_tenant',
        )


class BeautifulUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(BeautifulUserCreationForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
    )
    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=_('Enter the same password as before, for verification.'),
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')
        
    
    
class BeautifulSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(BeautifulSetPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_('New password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )


class BeautifulPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(BeautifulPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
    )
    
class BeautifulPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(BeautifulPasswordChangeForm, self).__init__(*args, **kwargs)

    old_password = forms.CharField(
        label=_('Old password'),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_('New password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )