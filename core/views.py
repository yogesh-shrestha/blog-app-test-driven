from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.views import (LoginView, 
                                       LogoutView, 
                                       PasswordChangeView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView
                                       )
from .forms import (SignUpForm, 
                    SignInForm, 
                    UserPasswordChangeForm, 
                    UserPasswordResetForm,
                    UserPasswordConfirmForm)


class UserSignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = "core/register.html"
    success_url = reverse_lazy('core:sign_in_page')


class UserSignInView(LoginView):
    form_class = SignInForm
    template_name = 'core/login.html'
    next_page = reverse_lazy('blog:index_page')


class UserLogoutView(LogoutView):
    template_name = 'core/logout.html'
    next_page = reverse_lazy('core:logout_page')


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'core/password_change.html'
    success_url = reverse_lazy('blog:index_page')


class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'core/password_reset.html'
    email_template_name='core/password_reset_email.html'
    success_url = reverse_lazy('core:password_reset_done_page')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'core/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'core/password_reset_confirm.html'
    form_class = UserPasswordConfirmForm
    success_url = reverse_lazy('core:password_reset_complete_page')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'core/password_reset_complete.html'
