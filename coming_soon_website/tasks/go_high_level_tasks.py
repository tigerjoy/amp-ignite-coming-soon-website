from background_task import background

from coming_soon_website.scripts import go_high_level_helper
from coming_soon_website.models import ContactFormData

def handle_task(func, arguments, service_name):
    try:
        return func(*arguments)
    except go_high_level_helper.AccessTokenExpiredException as a:
        try:
            go_high_level_helper.refresh_access_token(service_name)
            return func(*arguments)
        except Exception as e:
            raise
    except Exception as e:
        raise

# Add a contact and conversation for a Contact Form Submission
@background(schedule=0)
def save_contact_flow(contact_form_data_id: int, service_name):
    tasks = [
        go_high_level_helper.create_contact,
        go_high_level_helper.create_conversation,
        go_high_level_helper.add_inbound_conversation_message
    ]

    arguments = (service_name, contact_form_data_id)

    # Refresh the token if expired
    try:
        if not go_high_level_helper.is_access_token_valid(service_name):
            go_high_level_helper.refresh_access_token(service_name)
    except Exception as e:
        # Give up! Fail silently!
        print(e)
        return
    
    # Perform each task one by one
    for task in tasks:
        try:
            handle_task(task, arguments, service_name)
        except Exception as e:
            # Give up! Fail silently!
            print(e)
            return
    
    contact_form_data = ContactFormData.objects.filter(id=contact_form_data_id).first()
    if contact_form_data:
        contact_form_data.saved_in_gohighlevel = True
        contact_form_data.save()
