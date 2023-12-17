from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_email(email,email_token):
    subject = 'your accounts need to be verified'
    email_from = settings.EMAIL_HOST_USER
    message = f'Hello, Click on the link to activate your account http://127.0.0.1:8000/api/user/activate/{email_token}'
    
    send_mail(subject, message, email_from, [email])

def send_account_reset_email(email,email_token,uid):
    subject = 'To reset your password'
    email_from = settings.EMAIL_HOST_USER
    message = f'Hello, Click on the link to Reset your account http://127.0.0.1:8000/user/api/reset-password/{uid}/{email_token}'
    
    send_mail(subject, message, email_from, [email])