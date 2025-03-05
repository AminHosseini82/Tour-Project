from datetime import datetime
import jdatetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def logout_email(to_email):
    subject = '😢 خروج از سایت'
    # دریافت زمان فعلی
    current_time = datetime.now()
    # فرمت‌دهی به ساعت و دقیقه
    formatted_time = current_time.strftime('%H:%M')
    # دریافت تاریخ فعلی به میلادی
    # current_time = datetime.now()
    # تبدیل تاریخ میلادی به شمسی
    current_jdate = jdatetime.datetime.fromgregorian(datetime=current_time)
    formatted_jdate = current_jdate.strftime('%Y-%m-%d')  # فرمت: سال-ماه-روز

    context = {
        "logout_time": formatted_time,
        "tarik": formatted_jdate
    }
    html_message = render_to_string('accounts/email_sending/logout_email.html', context)
    plain_message = strip_tags(html_message)
    from_email = "aminhosseini822003@gmail.com"
    to = to_email
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
