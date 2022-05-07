from django.urls import path
from .views import ProfileView, LoginView, SignUpView
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from .forms import BeautifulPasswordChangeForm, BeautifulPasswordResetForm, BeautifulSetPasswordForm
app_name = 'user'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password_change/',
         PasswordChangeView.as_view(template_name='users/password_change.html', form_class=BeautifulPasswordChangeForm),
         name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/',
         PasswordResetView.as_view(template_name='users/password_reset.html', form_class=BeautifulPasswordResetForm),
         name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                                                     form_class=BeautifulSetPasswordForm),
         name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
