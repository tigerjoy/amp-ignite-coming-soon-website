from django.db import models
from django.utils import timezone

# Create your models here.
class ContactFormData(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    name = models.TextField(blank=False, null=False)
    company = models.TextField(blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    phone = models.CharField(max_length=20, blank=False, null=False)
    customer_message = models.TextField(blank=False, null=False)
    ip_address = models.CharField(max_length=50, blank=False, null=False)
    timezone = models.CharField(max_length=50, blank=False, null=False)
    website_type = models.CharField(max_length=255, blank=False, null=False)
    form_type = models.CharField(max_length=255, blank=False, null=False)
    saved_in_gohighlevel = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"ContactFormData("
            f"id={self.id}"
            f"name={self.name}, "
            f"company={self.company}, "
            f"email={self.email}, "
            f"phone={self.phone}, "
            f"customer_message={self.customer_message}, "
            f"ip_address={self.ip_address}, "
            f"timezone={self.timezone}, "
            f"website_type={self.website_type}, "
            f"form_type={self.form_type})"
            f"saved_in_gohighlevel={self.saved_in_gohighlevel})"
        )

class ApiToken(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    service_name = models.TextField(null=False, blank=False)
    access_token = models.TextField(null=False, blank=False)
    refresh_token = models.TextField(null=False, blank=False)
    location_id = models.TextField(null=False, blank=False)
    expires_in = models.DateTimeField(null=False, blank=False)
    json_response = models.JSONField(null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"ApiToken("
            f"id={self.id}, "
            f"service_name={self.service_name}, "
            f"access_token={self.access_token}, "
            f"refresh_token={self.refresh_token}, "
            f"location_id={self.location_id}, "
            f"expires_in={self.expires_in}, "
            f"json_response={self.json_response}"
            f"created_at={self.created_at}"
            f"modified_at={self.modified_at}"
            f")"
        )
    
class ApiTokenRefreshLog(models.Model):
    id = models.AutoField(primary_key=True)
    api_token = models.ForeignKey('ApiToken', on_delete=models.PROTECT)
    is_refresh_successful = models.BooleanField(default=False)
    error_log = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return (
            f"ApiTokenRefreshLog(id={self.id}, "
            f"api_token_id={self.api_token_id}, "
            f"is_refresh_successful={self.is_refresh_successful}, "
            f"error_log={self.error_log}, "
            f"created_at={self.created_at})"
        )
