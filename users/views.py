from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from .forms import BeautifulAuthenticationForm, UserForm, BeautifulUserCreationForm
from django.urls import reverse


def get_user_profile(request) -> dict:
    user = (
        get_user_model()
        .objects.filter(email=request.user.email)
        .only(
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'mobile_number',
            'avatar',
            'role',
        )
        .first()
    )
    user_form = UserForm(instance=request.user)
    context = {'user': user, 'user_form': user_form}
    return context


class SignUpView(View):
    def get(self, request):
        template = 'users/signup.html'
        context = {'form': BeautifulUserCreationForm()}
        return render(request, template, context)

    def post(self, request):
        form = BeautifulUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('user:profile'))
        else:
            return self.get(request)


@method_decorator(login_required, name='get')
class ProfileView(View):
    def get(self, request):
        template = 'users/profile.html'
        context = get_user_profile(request)
        return render(request, template, context)

    def post(self, request):
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = request.user
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.middle_name = form.cleaned_data['middle_name']
            user.role = form.cleaned_data['role']
            user.mobile_number = form.cleaned_data['mobile_number']
            user.save()
            return redirect(reverse('user:profile'))
        else:
            return self.get(request)


class LoginView(View):
    def get(self, request):
        template = 'users/login.html'
        form = BeautifulAuthenticationForm()
        context = {'form': form, 'user': request.user}
        return render(request, template, context)

    def post(self, request):
        form = BeautifulAuthenticationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('user:profile'))
        return self.get(request)
