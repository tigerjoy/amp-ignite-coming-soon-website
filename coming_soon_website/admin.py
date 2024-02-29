from django.contrib import admin
from .models import NotificationFormData, ContactFormData, ApiToken, ApiCallErrorLog

# Register your models here.
admin.site.register(NotificationFormData)
admin.site.register(ContactFormData)
admin.site.register(ApiToken)
admin.site.register(ApiCallErrorLog)