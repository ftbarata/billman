from django.contrib import admin
from .models import BillingControl, ScheduledPrice, BillingHistory

admin.site.register(BillingControl)
admin.site.register(ScheduledPrice)
admin.site.register(BillingHistory)
