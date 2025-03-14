from django.shortcuts import render

from accounts.models import UserProfile
# from django.contrib.auth import login, logout
from email_sending.accounts.login_email.welcome_again import welcome_again_send_email
from email_sending.accounts.signin_code.welcome_first_time import welcome_send_email
from email_sending.accounts.logout_email.massage_logout import logout_email
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
from sms_sending import sms_test


# این درست بوده👇

# def signup_page(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         phone_number = request.POST['phone_number']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#
#         if password1 == password2:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request, "username taken...")
#                 return redirect('accounts:signup')
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request, "email taken...")
#                 return redirect('accounts:signup')
#             else:
#                 user = User.objects.create_user(username=username, password=password1, email=email)
#                 user.save()
#                 UserProfile.objects.create(user=user, phone_number=phone_number)
#                 messages.info(request, "user created...")
#                 welcome_send_email(user.email)
#                 return redirect('accounts:login')
#         else:
#             messages.info(request, "password not matched...")
#             return redirect('accounts:signup')
#     else:
#         return render(request, 'accounts/signup.html')

# این درست بوده👆


def signup_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone_number = request.POST['phone_number']  # فیلد اجباری

        if not phone_number:  # چک کردن اینکه شماره تلفن وارد شده باشه
            messages.info(request, "شماره تلفن اجباری است.")
            return redirect('accounts:signup')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "نام کاربری قبلاً گرفته شده است.")
                return redirect('accounts:signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "ایمیل قبلاً گرفته شده است.")
                return redirect('accounts:signup')
            elif UserProfile.objects.filter(phone_number=phone_number).exists():
                messages.info(request, "شماره تلفن قبلاً ثبت شده است.")
                return redirect('accounts:signup')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()
                UserProfile.objects.create(user=user, phone_number=phone_number)
                messages.info(request, "کاربر با موفقیت ساخته شد.")
                welcome_send_email(user.email)
                return redirect('accounts:login')
        else:
            messages.info(request, "رمزهای عبور مطابقت ندارند.")
            return redirect('accounts:signup')
    else:
        return render(request, 'accounts/signup.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            welcome_send_email(user.email)
            sms_test()
            return redirect('tour:main_page')
        else:
            messages.info(request, 'نام کاربری یا رمز عبور اشتباه است.')
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')


# این درست بوده👇
# def login_page(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#
#         user = auth.authenticate(username=username, password=password)
#
#         if user is not None:
#             auth.login(request, user)
#             welcome_again_send_email(user.email)
#             return redirect('tour:main_page')
#         else:
#             messages.info(request, 'invalid credentials...')
#             return redirect('accounts:login')
#     else:
#         return render(request, 'accounts/login.html')


# این درست بوده👆


def logout_page(request):
    if request.method == "POST":
        # user_email = request.user.email  # دریافت ایمیل کاربر
        user_email = request.session.get('user_email')
        logout(request)
        logout_email(user_email)
        return redirect('tour:main_page')
