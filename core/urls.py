from django.urls import path
from . import views

app_name='core'

urlpatterns = [
    path("sign-up/", views.UserSignUpView.as_view(), name='sign_up_page'),
    path("sign-in/", views.UserSignInView.as_view(), name='sign_in_page'),
    path("logout/", views.UserLogoutView.as_view(), name='logout_page'),
    path("password-change/", views.UserPasswordChangeView.as_view(), 
         name='password_change_page'),
    path("password-reset/", views.UserPasswordResetView.as_view(), 
         name='password_reset_page'),
    path("password-reset-done/", views.UserPasswordResetDoneView.as_view(), 
        name='password_reset_done_page'),
    path("password-reset/<uidb64>/<token>/", views.UserPasswordResetConfirmView.as_view(), 
        name='password_reset_confirm_page'),
    path("password-reset-complete/", views.UserPasswordResetCompleteView.as_view(), 
        name='password_reset_complete_page'),
]