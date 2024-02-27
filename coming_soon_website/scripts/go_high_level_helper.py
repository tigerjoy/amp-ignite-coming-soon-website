import requests
import json
import traceback
import requests

from django.utils import timezone
from django.conf import settings
from datetime import timedelta

from coming_soon_website.models import ApiToken, ContactFormData, ApiCallErrorLog


# Define all API endpoints with their respective payload
# and headers structure
API_ENDPOINTS = {
    "refresh_access_token": {
        "url": "https://services.leadconnectorhq.com/oauth/token",
        "method": "POST",
        "payload": {
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": ""
        },
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
    },
    "write_contact": {
        "url": "https://services.leadconnectorhq.com/contacts/",
        "method": "POST",
        "payload": {
            "name": "",
            "email": "",
            "locationId": "",
            "phone": "",
            "timezone": "",
            "tags": [],
            "customFields": [
                # {
                #     "id": "6dvNaf7VhkQ9snc5vnjJ", // id OR key
                #     "key": "my_custom_field", // id OR key
                #     "field_value": "9039160788"
                # }
            ],
            "source": "",
            "companyName": ""
        },
        "headers": {
            "Authorization": "Bearer <token>",
            "Version": "2021-07-28",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    },
    "write_conversation": {
        "url": "https://services.leadconnectorhq.com/conversations/",
        "method": "POST",
        "payload": {
            "locationId": "",
            "contactId": "",
        },
        "headers": {
            "Authorization": "Bearer <token>",
            "Version": "2021-04-15",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    },
    "add_inbound_conversation_message": {
        "url": "https://services.leadconnectorhq.com/conversations/messages/inbound",
        "method": "POST",
        "payload": {
            "type": "Email", # There are more types like SMS, WhatsApp, GMB, IG, FB, Custom, WebChat, Live_Chat
            "message": "",
            "conversationId": "",
            "html": "",
            "subject": "",
            "emailFrom": "",
            "emailTo": "",
            "emailCc": [],
            "emailBcc": [],
            "direction": "inbound",
            "date": "" # Should be in ISO format ex. 2019-08-24T14:15:22Z
        },
        "headers": {
            "Authorization": "Bearer <token>",
            "Version": "2021-04-15",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    }
}

# Add all custom exception classes
class CreateContactException(Exception):
    def __init__(self, status_code, response_text):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"CreateContactException(status_code={status_code}, response_text={response_text})")

    def __str__(self):
        return f"CreateContactException(status_code={self.status_code}, response_text={self.response_text})"
    
class CreateConversationException(Exception):
    def __init__(self, status_code, response_text):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"CreateConversationException(status_code={status_code}, response_text={response_text})")

    def __str__(self):
        return f"CreateConversationException(status_code={self.status_code}, response_text={self.response_text})"

class AddInboundConversationMessageException(Exception):
    def __init__(self, status_code, response_text):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"AddInboundConversationMessageException(status_code={status_code}, response_text={response_text})")

    def __str__(self):
        return f"AddInboundConversationMessageException(status_code={self.status_code}, response_text={self.response_text})"

class AccessTokenExpiredException(Exception):
    def __init__(self, status_code, response_text):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"AccessTokenExpiredException(status_code={status_code}, response_text={response_text})")

    def __str__(self):
        return f"AccessTokenExpiredException(status_code={self.status_code}, response_text={self.response_text})"

def call_api(endpoint_key, custom_payload=None, custom_headers=None):
    endpoint_config = API_ENDPOINTS.get(endpoint_key)
    if not endpoint_config:
        raise ValueError(f"Endpoint '{endpoint_key}' not found in API_ENDPOINTS")

    url = endpoint_config["url"]
    method = endpoint_config["method"]
    payload = {**endpoint_config.get("payload", {}), **(custom_payload or {})}
    headers = {**endpoint_config.get("headers", {}), **(custom_headers or {})}

    print("payload")
    print(json.dumps(payload, indent=4))

    print("headers")
    print(json.dumps(headers, indent=4))

    try:
        if method == "GET":
            response = requests.get(url, params=payload, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=payload, headers=headers)

        return response  # Assuming the API returns JSON data
    except requests.exceptions.RequestException as e:
        # Handle API call failure
        print(f"Failed to call API '{endpoint_key}': {e}")
        raise  # Reraise the exception to stop further processing

def is_access_token_valid(service_name):
    service_token_record = ApiToken.objects.filter(service_name=service_name).first()

    if not service_token_record:
        return False
    else:
        threshold_time = timezone.now() + timedelta(minutes=settings.TOKEN_REFRESH_THRESHOLD_MINUTES)

        # If the token expires in the future
        if threshold_time < service_token_record.expires_in:
            return True
        else:
            return False

def refresh_access_token(service_name):
    ENDPOINT_KEY = "refresh_access_token"

    if not service_name:
        print("service_name is invalid")
        return
    
    service_token_record = ApiToken.objects.filter(service_name=service_name).first()

    if not service_token_record:
        print(f"Did not find a service_token_record associated with {service_name}")
        return
    
    payload = {
        "refresh_token": service_token_record.refresh_token
    }

    try:
        response = call_api(ENDPOINT_KEY, payload)

        if response.status_code in [200]:
            json_response = response.json()
            service_token_record.access_token = json_response["access_token"]
            service_token_record.refresh_token = json_response["refresh_token"]
            service_token_record.expires_in = timezone.now() + timedelta(seconds=int(json_response["expires_in"]))
            service_token_record.json_response = json.dumps(json_response, ensure_ascii=False)
            service_token_record.save()
            print("Successfully refreshed access token and updated in DB")
            print(service_token_record)
        else:
            print("Request failed, could not refresh access token")
            print(response)
            print(response.text)
            refresh_error_log = ApiCallErrorLog(
                api_token=service_token_record
            )
            error_log = json.dumps({
                "status_code": response.status_code,
                "response_text": response.text
            })
            refresh_error_log.error_log = error_log
            refresh_error_log.error_type = "AuthTokenRefreshException"
            refresh_error_log.save()
    except Exception as e:
        refresh_error_log = ApiCallErrorLog(
            api_token=service_token_record
        )
        error_log = json.dumps({
           "error": str(e),
           "traceback":  traceback.format_exc()
        })
        refresh_error_log.error_log = error_log
        refresh_error_log.error_type = "GenericException"
        refresh_error_log.save()

def create_contact(service_name, contact_form_data_id: int):
    ENDPOINT_KEY = "write_contact"

    if not contact_form_data_id:
        print("contact_form_data_id is invalid, cannot create contact!")
        return
    
    contact_form_data = ContactFormData.objects.filter(id=contact_form_data_id).first()

    if not contact_form_data:
        print("contact_form_data is invalid, cannot create contact!")
        return False
    
    service_token_record = ApiToken.objects.filter(service_name=service_name).first()

    if not service_token_record:
        print(f"Did not find a service_token_record associated with {service_name}")
        return

    payload = {
        "name": contact_form_data.name,
        "email": contact_form_data.email,
        "locationId": service_token_record.location_id,
        "phone": contact_form_data.phone,
        "timezone": contact_form_data.timezone,
        "tags": [
            contact_form_data.website_type,
            contact_form_data.form_type
        ],
        "customFields": [
            {
                "key": "customer_message",
                "field_value": contact_form_data.customer_message
            },
            {
                "key": "website_type",
                "field_value": contact_form_data.website_type
            },
            {
                "key": "form_type",
                "field_value": contact_form_data.form_type
            }
        ],
        "source": contact_form_data.website_type + "|" + contact_form_data.form_type,
        "companyName": contact_form_data.company
    }

    headers = {
        "Authorization": f"Bearer {service_token_record.access_token}"
    }

    try:
        response = call_api(ENDPOINT_KEY, payload, headers)

        if response.status_code in [201, 200]:
            json_response = response.json()
            print(json_response)
            if "contact" in json_response and "id" in json_response["contact"]:
                contact_form_data.contact_id = json_response["contact"]["id"]     
            contact_form_data.save()
            return True
        elif response.status_code in [401]:
            raise AccessTokenExpiredException(status_code=response.status_code, response_text=response.text)
        else:
            raise CreateContactException(status_code=response.status_code, response_text=response.text)
    except AccessTokenExpiredException as a:
        api_call_error_log = ApiCallErrorLog(
            api_token=service_token_record,
            contact_form_data=contact_form_data
        )
        api_call_error_log.error_log = json.dumps({
            "status_code": a.status_code,
            "response_text": a.response_text
        })
        api_call_error_log.error_type = type(a).__name__
        api_call_error_log.save()
        raise
    except CreateContactException as c:
        api_call_error_log = ApiCallErrorLog(
            api_token=service_token_record,
            contact_form_data=contact_form_data
        )
        api_call_error_log.error_log = json.dumps({
            "status_code": c.status_code,
            "response_text": c.response_text
        })
        api_call_error_log.error_type = type(c).__name__
        api_call_error_log.save()
        raise
    except Exception as e:
        print(e)
        api_call_error_log = ApiCallErrorLog(
            api_token=service_token_record,
            contact_form_data=contact_form_data
        )
        error_log = json.dumps({
           "error": str(e),
           "traceback":  traceback.format_exc()
        })
        api_call_error_log.error_log = error_log
        api_call_error_log.error_type = "GenericException"
        api_call_error_log.save()
        raise

def create_conversation(service_name, contact_form_data_id: int):
    ENDPOINT_KEY = "write_conversation"

    if not contact_form_data_id:
        print("contact_form_data_id is invalid, cannot create contact!")
        return
    
    contact_form_data = ContactFormData.objects.filter(id=contact_form_data_id).first()

    if not contact_form_data:
        print("contact_form_data is invalid, cannot create contact!")
        return False
    
    service_token_record = ApiToken.objects.filter(service_name=service_name).first()

    if not service_token_record:
        print(f"Did not find a service_token_record associated with {service_name}")
        return
    
    payload = {
        "locationId": service_token_record.location_id,
        "contactId": contact_form_data.contact_id
    }

    headers = {
        "Authorization": f"Bearer {service_token_record.access_token}"
    }

    try:
        response = call_api(ENDPOINT_KEY, payload, headers)

        if response.status_code in [201, 200]:
            json_response = response.json()
            print(json_response)

            if "success" not in json_response or not json_response["success"]:
                return False

            if "conversation" in json_response and "id" in json_response["conversation"]:
                contact_form_data.conversation_id = json_response["conversation"]["id"]     
            contact_form_data.save()
            return True
        elif response.status_code in [401]:
            raise AccessTokenExpiredException(status_code=response.status_code, response_text=response.text)
        else:
            raise CreateConversationException(status_code=response.status_code, response_text=response.text)
    except AccessTokenExpiredException as a:
        api_call_error_log = ApiCallErrorLog(
            api_token=service_token_record,
            contact_form_data=contact_form_data
        )
        api_call_error_log.error_log = json.dumps({
            "status_code": a.status_code,
            "response_text": a.response_text
        })
        api_call_error_log.error_type = type(a).__name__
        api_call_error_log.save()
        raise
    except CreateContactException as c:
        api_call_error_log = ApiCallErrorLog(
            api_token=service_token_record,
            contact_form_data=contact_form_data
        )
        api_call_error_log.error_log = json.dumps({
            "status_code": c.status_code,
            "response_text": c.response_text
        })
        api_call_error_log.error_type = type(c).__name__
        api_call_error_log.save()
        raise
    except Exception as e:
        print(e)
        api_call_error_log = ApiCallErrorLog(
            api_token=service_token_record
        )
        error_log = json.dumps({
           "error": str(e),
           "traceback":  traceback.format_exc()
        })
        api_call_error_log.error_log = error_log
        api_call_error_log.error_type = "GenericException"
        api_call_error_log.save()
        raise

def add_inbound_conversation_message(service_name, contact_form_data_id: int):
    ENDPOINT_KEY = "add_inbound_conversation_message"

    if not contact_form_data_id:
        print("contact_form_data_id is invalid, cannot create contact!")
        return
    
    contact_form_data = ContactFormData.objects.filter(id=contact_form_data_id).first()

    if not contact_form_data:
        print("contact_form_data is invalid, cannot create contact!")
        return False
    
    service_token_record = ApiToken.objects.filter(service_name=service_name).first()

    if not service_token_record:
        print(f"Did not find a service_token_record associated with {service_name}")
        return
    
    payload = {
        "type": "Email",
        "message": contact_form_data.customer_message,
        "conversationId": contact_form_data.conversation_id,
        "html": f"<p>{contact_form_data.customer_message}</p>",
        "subject": "[INQUIRY] From Contact Form",
        "emailFrom": contact_form_data.email,
        "emailTo": settings.EMAIL_TO[0] if len(settings.EMAIL_TO) >= 1 else [],
        "emailCc": settings.EMAIL_TO[1:] if len(settings.EMAIL_TO) >= 2 else [],
        "direction": "inbound",
        "date": timezone.now().isoformat() 
    }

    headers = {
        "Authorization": f"Bearer {service_token_record.access_token}"
    }

    try:
        response = call_api(ENDPOINT_KEY, payload, headers)

        if response.status_code in [201, 200]:
            json_response = response.json()
            print(json_response)

            if "success" not in json_response or not json_response["success"]:
                return False

            if "messageId" in json_response:
                contact_form_data.message_id = json_response["messageId"]

            if "emailMessageId" in json_response:
                contact_form_data.email_message_id = json_response["emailMessageId"]

            contact_form_data.save()
            return True
        elif response.status_code in [401]:
            raise AccessTokenExpiredException(status_code=response.status_code, response_text=response.text)
        else:
            raise AddInboundConversationMessageException(status_code=response.status_code, response_text=response.text)
    except AccessTokenExpiredException as a:
        api_call_error_log = ApiCallErrorLog(
            api_token=service_token_record,
            contact_form_data=contact_form_data
        )
        api_call_error_log.error_log = json.dumps({
            "status_code": a.status_code,
            "response_text": a.response_text
        })
        api_call_error_log.error_type = type(a).__name__
        api_call_error_log.save()
        raise
    except CreateContactException as c:
        api_call_error_log = ApiCallErrorLog(
            api_token=service_token_record,
            contact_form_data=contact_form_data
        )
        api_call_error_log.error_log = json.dumps({
            "status_code": c.status_code,
            "response_text": c.response_text
        })
        api_call_error_log.error_type = type(c).__name__
        api_call_error_log.save()
        raise
    except Exception as e:
        print(e)
        api_call_error_log = ApiCallErrorLog(
            api_token=service_token_record
        )
        error_log = json.dumps({
           "error": str(e),
           "traceback":  traceback.format_exc()
        })
        api_call_error_log.error_log = error_log
        api_call_error_log.error_type = "GenericException"
        api_call_error_log.save()
        raise