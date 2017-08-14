from django.contrib import admin
from .models import BillingControl, ScheduledPrice

admin.site.register(BillingControl)
admin.site.register(ScheduledPrice)
