from django.http import HttpResponse
from django.shortcuts import render
from accounts.models import UserProfile
from email_sending.accounts.signin_code.welcome_first_time import welcome_send_email
from email_sending.accounts.logout_email.massage_logout import logout_email
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
import random
from sms_sending.source_code import sms_test


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
                # return redirect('accounts:login')
                # Login to site
                user = auth.authenticate(username=username, password=password1)
                auth.login(request, user)
                return redirect("main_page")
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
            # sms_test()
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


# this function choses the Authentication way, SMS or Email
def choose_auth_method(request):
    return render(request, "accounts/sms_view/choose_auth_method.html")


def review_password_sms_input(request):
    if request.method == 'POST':
        user_mobile = request.POST.get('phone')
        result = UserProfile.objects.filter(phone_number=user_mobile).exists()
        if result:
            random_number = random.randrange(100000, 999999)
            message = f"این شماره احراز هویت شما میباشد {random_number}. لغو11"
            sms_test(user_mobile, message)
            request.session['sms_code'] = random_number
            request.session['phone_number'] = user_mobile  # ذخیره شماره موبایل
            context = {
                "random_number": random_number,
            }
            return render(request, "accounts/sms_view/review_password_sms_sendSMS.html", context)
        else:
            context = {
                "eroer_text": "این شماره در سایت ثبت‌نام نکرده است."
            }
            return render(request, 'accounts/sms_view/review_password_sms_sendSMS.html', context)

    return render(request, 'accounts/sms_view/review_password_sms_inputNumber.html')


def verify_sms_code(request):
    if request.method == "POST":
        entered_code = request.POST.get("code")
        expected_code = request.session.get('sms_code')
        phone_number = request.session.get('phone_number')

        if not phone_number or not expected_code:
            return HttpResponse("اطلاعات احراز هویت موجود نیست.", status=400)

        if entered_code == str(expected_code):
            # کد درست است، فقط sms_code رو پاک می‌کنیم و phone_number رو نگه می‌داریم
            del request.session['sms_code']
            return redirect("accounts:review_password_sms_inputPassword")
        else:
            context = {
                "random_number": expected_code,
                "error": "کد وارد‌شده اشتباه است."
            }
            return render(request, "accounts/sms_view/review_password_sms_sendSMS.html", context)

    return HttpResponse("روش درخواست نامعتبر است.", status=405)


def review_password_sms_inputPassword(request):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        phone_number = request.session.get('phone_number')

        # چک کردن اینکه phone_number وجود داره
        if not phone_number:
            return render(request, "accounts/sms_view/error_page.html", {
                "error": "شماره تلفن در دسترس نیست. لطفاً دوباره شروع کنید."
            })

        if new_password == confirm_password:
            try:
                user_profile = UserProfile.objects.get(phone_number=phone_number)
                user = user_profile.user
                user.set_password(new_password)
                user.save()
                # بعد از ذخیره رمز، session رو پاک می‌کنیم
                del request.session['phone_number']
                return render(request, "accounts/sms_view/password_change_success.html")
            except UserProfile.DoesNotExist:
                return render(request, "accounts/sms_view/error_page.html", {
                    "error": "کاربر با این شماره پیدا نشد."
                })
        else:
            return render(request, "accounts/sms_view/review_password_sms_inputPassword.html", {
                "error": "رمز عبور و تأیید آن یکسان نیستند."
            })

    return render(request, "accounts/sms_view/review_password_sms_inputPassword.html")
