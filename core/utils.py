from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(user, otp_code):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp_code}. It will expire in 10 minutes.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    
    send_mail(subject, message, email_from, recipient_list)
