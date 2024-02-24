from django.core.management.base import BaseCommand
import coming_soon_website.scripts.go_high_level_helper as ghlh

class Command(BaseCommand):
    help = 'Commands for testing management scripts'

    def handle(self, *args, **kwargs):
        is_access_token_valid = ghlh.is_access_token_valid("GoHighLevel.ContactFormSubmission")
        print("Is access token valid?", is_access_token_valid)
        
        if is_access_token_valid:
            ghlh.refresh_access_token("GoHighLevel.ContactFormSubmission")

