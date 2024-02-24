from django.db import models

# Create your models here.
class ContactFormData(models.Model):
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
