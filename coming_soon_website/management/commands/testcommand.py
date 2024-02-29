from django.core.management.base import BaseCommand
import coming_soon_website.scripts.go_high_level_helper as ghlh
from coming_soon_website.models import ContactFormData
from coming_soon_website.tasks.go_high_level_tasks import save_contact_flow

class Command(BaseCommand):
    help = 'Commands for testing management scripts'

    def handle(self, *args, **kwargs):
        SERVICE_NAME = "GoHighLevel.ContactFormSubmission"
        contact_form_data_id = 4

        save_contact_flow.now(contact_form_data_id=contact_form_data_id, service_name=SERVICE_NAME)
        # is_access_token_valid = ghlh.is_access_token_valid(SERVICE_NAME)

        # print("Is access token valid?", is_access_token_valid)
        
        # if not is_access_token_valid or True:
        #     ghlh.refresh_access_token("GoHighLevel.ContactFormSubmission")
        
        # ghlh.create_contact("GoHighLevel.ContactFormSubmission", contact_form_data_id=3)
        # ghlh.create_conversation("GoHighLevel.ContactFormSubmission", contact_form_data_id=3)
        # ghlh.add_inbound_conversation_message("GoHighLevel.ContactFormSubmission", contact_form_data_id=3)

