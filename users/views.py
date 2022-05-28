from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from .forms import BeautifulAuthenticationForm, UserForm, BeautifulUserCreationForm, TenantForm, LessorForm, DepositForm
from django.urls import reverse
from core.decorators import tenant_required, lessor_required
from django.contrib import messages
from malls.models import Rent, Mall
from users.models import TenantProfile


def get_user_profile(request) -> dict:
    user = (
        get_user_model()
            .objects.filter(email=request.user.email)
            .only(
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "mobile_number",
            "avatar",
        )
            .first()
    )
    user_form = UserForm(instance=request.user)
    context = {"user": user, "user_form": user_form}
    return context


class SignUpView(View):
    def get(self, request):
        template = "users/signup.html"
        context = {"form": BeautifulUserCreationForm()}
        return render(request, template, context)

    def post(self, request):
        form = BeautifulUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("user:profile"))
        else:
            return self.get(request)


@method_decorator(login_required, name="get")
class ProfileView(View):
    def get(self, request):
        template = "users/profile.html"
        context = get_user_profile(request)
        return render(request, template, context)

    def post(self, request):
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = request.user
            user.email = form.cleaned_data["email"]
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.middle_name = form.cleaned_data["middle_name"]
            user.mobile_number = form.cleaned_data["mobile_number"]
            user.is_lessor = form.cleaned_data["is_lessor"]
            user.is_tenant = form.cleaned_data["is_tenant"]
            user.save()
            messages.info(request, 'Профиль обновлен успешно')
            return redirect(reverse("user:profile"))
        else:
            messages.error(request, 'Произошла ошибка, перепроверьте вводимые данные.')
            return self.get(request)


class LoginView(View):
    def get(self, request):
        template = "users/login.html"
        form = BeautifulAuthenticationForm()
        context = {"form": form, "user": request.user}
        return render(request, template, context)

    def post(self, request):
        form = BeautifulAuthenticationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("user:profile"))
        return self.get(request)


@method_decorator(lessor_required, name="get")
class LessorView(View):
    def get(self, request):
        template = "users/lessor.html"
        form = TenantForm(instance=request.user.lessor_profile)
        my_mall = Mall.objects.filter(owner=request.user).prefetch_related('areas')
        context = {"my_mall": my_mall, "form": form}
        return render(request, template, context)

    def post(self, request):
        form = LessorForm(request.POST, instance=request.user)
        if form.is_valid():
            user = request.user.lessor_profile
            user.contacts_and_over_information = form.cleaned_data["contacts_and_over_information"]
            user.save()
            return redirect(reverse("user:lessor_profile"))
        else:
            return self.get(request)


@method_decorator(tenant_required, name="get")
class TenantView(View):
    def get(self, request):
        template = "users/tenant.html"
        form = TenantForm(instance=request.user.tenant_profile)
        active_rent = Rent.objects.filter(
            tenant=request.user).filter(status=True).select_related('area').only('balance', 'rental_start_date_time',
                                                                                 'area__id', 'area__mall__id')
        tenant = TenantProfile.objects.filter(user_id=request.user.id).only('balance').first()
        context = {"active_rent": active_rent, "form": form, "tenant": tenant}
        return render(request, template, context)

    def post(self, request):
        form = TenantForm(request.POST, instance=request.user)
        if form.is_valid():
            user = request.user.tenant_profile
            user.contacts_and_over_information = form.cleaned_data["contacts_and_over_information"]
            user.save()
            return redirect(reverse("user:tenant_profile"))
        else:
            return self.get(request)


@method_decorator(tenant_required, name="get")
class DepositView(View):
    def get(self, request):
        template = 'users/deposit.html'
        form = DepositForm()
        context = {'form': form}
        return render(request, template, context)

    def post(self, request):
        form = DepositForm(request.POST)
        if form.is_valid():
            tenant = request.user.tenant_profile
            tenant.balance += form.cleaned_data['deposit']
            tenant.save()
            return redirect(reverse("user:tenant_profile"))
        else:
            return self.get(request)
