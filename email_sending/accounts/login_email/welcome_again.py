from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def welcome_again_send_email(to_email):
    subject = '✨ سفر به دنیای شگفت‌انگیز ما! 🌍✈️'
    html_message = render_to_string('accounts/email_sending/login_welcome_email.html')
    plain_message = strip_tags(html_message)
    from_email = "aminhosseini822003@gmail.com"
    to = to_email
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
