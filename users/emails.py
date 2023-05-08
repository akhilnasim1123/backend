from django.core.mail import send_mail
import random
from django.conf import settings
from .models import OTP, UserAccount


def sent_otp_via_email(email):
    subject = 'Please Verify Your Email Address'
    otp = random.randint(1000,9999)
    message = f'Your Verification OTP is {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from,[email])
    # user = UserAccount.objects.get(email=email)
    verify = OTP.objects.filter(email=email).exists()
    if verify:
        OTP.objects.filter(email=email).delete()
    otp_registration = OTP.objects.create(
        # user = user,
        otp = otp,
        email=email,
    )
    otp_registration.save()
    return otp


def sent_otp_for_emailVerify(email):
    subject = 'Please Verify Your Email Address'
    otp = random.randint(1000,9999)
    message = f'Your Verification OTP is {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from,[email])
    user = UserAccount.objects.get(email=email)
    verify = OTP.objects.filter(email=email).exists()
    if verify:
        OTP.objects.filter(email=email).delete()
    otp_registration = OTP.objects.create(
        # user = user,
        otp = otp,
        email=email,
    )

    otp_registration.save()
    return otp
    