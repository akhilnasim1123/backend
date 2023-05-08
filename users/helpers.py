import random
from django.core.cache import cache

from .models import OTP, UserAccount

def sent_otp_to_mobile(mobile):
    if cache.get(mobile):
        return False
    try:
        otp_to_sent = random.randint(1000,9999)
        cache.set(mobile,otp_to_sent,timeout=60)
        user = UserAccount.objects.get(phone_number=mobile)
        user.otp = otp_to_sent
        otp_registration = OTP.objects.create(
        user = user,
        otp = otp_to_sent,
    )
        otp_registration.save()
        user.save()
    except Exception as e:
        print(e)