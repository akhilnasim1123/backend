from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(UserAccount),
admin.site.register(BlogIdea),
admin.site.register(BlogSection),
admin.site.register(Prime),
admin.site.register(PremiumSubscription),