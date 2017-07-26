from django.contrib import admin
from .models import Service, CustomerDetails, CustomerPhone

admin.site.register(Service)
admin.site.register(CustomerDetails)
admin.site.register(CustomerPhone)