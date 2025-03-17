from datetime import datetime
import jdatetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def warining_smsCredit_low():
    subject = 'هشدار کاهش اعتبار پیامکی قاصدک ⚠'
    html_message = render_to_string('warning_smsCredit_low.html')
    plain_message = strip_tags(html_message)
    from_email = "aminhosseini822003@gmail.com"
    to = "aminhosseini822003@gmail.com"
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
