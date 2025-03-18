from django.contrib import admin
from django.urls import path
from .views import signup_page, login_page, logout_page
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy  # اضافه کردن این خط
from .views import review_password_sms_input, review_password_sms_inputPassword

app_name = 'accounts'
urlpatterns = [
    path("signup/", signup_page, name="signup"),
    path("login/", login_page, name="login"),
    path("logout/", logout_page, name="logout"),

    path("choose_auth_method/", views.choose_auth_method, name="choose_auth_method"),

    path("review_password_sms_input/", review_password_sms_input, name="review_password_sms_input"),
    path("review_password_sms_inputPassword/", review_password_sms_inputPassword,
         name="review_password_sms_inputPassword"),
    path("verify_sms/", views.verify_sms_code, name="verify_sms_code"),
    # reset password URL
    # path("login/reset_password/", auth_views.PasswordResetView.as_view(),
    #      name="reset_password"),
    # path("login/reset_password_sent/",
    #      auth_views.PasswordResetDoneView.as_view(),
    #      name="password_reset_done"),
    # path("login/reset/<uidb64>/<token>/",
    #      auth_views.PasswordResetConfirmView.as_view(),
    #      name="password_reset_confirm"),
    # path("login/reset_password_complete/",
    #      auth_views.PasswordResetCompleteView.as_view(),
    #      name="password_reset_complete"),

    path("login/reset_password/", auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html",
        success_url=reverse_lazy('accounts:password_reset_done'),  # اضافه کردن این خط
        email_template_name="accounts/password_reset_email.html"  # اگه قالب سفارشی ساختید
    ), name="reset_password"),

    # path("login/reset_password/", auth_views.PasswordResetView.as_view(
    #     template_name="accounts/password_reset.html",
    #     email_template_name="accounts/password_reset_email.html"  # اضافه کردن این خط
    # ), name="reset_password"),

    # path("login/reset_password/", auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
    #      name="reset_password"),
    path("login/reset_password_sent/",
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path("login/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_form.html",
        success_url=reverse_lazy('accounts:password_reset_complete')  # اضافه کردن این خط
    ), name="password_reset_confirm"),

    # path("login/reset/<uidb64>/<token>/",
    #      auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
    #      name="password_reset_confirm"),
    path("login/reset_password_complete/",
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),

]
