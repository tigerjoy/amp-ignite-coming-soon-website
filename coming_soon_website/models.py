from django.db import models

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
    expires_in = models.DateTimeField(null=False, blank=False)
    json_response = models.JSONField(null=False, blank=False)

    def __str__(self):
        return (
            f"ApiToken("
            f"id={self.id}, "
            f"service_name={self.service_name}, "
            f"access_token={self.access_token}, "
            f"refresh_token={self.refresh_token}, "
            f"expires_in={self.expires_in}, "
            f"json_response={self.json_response}"
            f")"
        )