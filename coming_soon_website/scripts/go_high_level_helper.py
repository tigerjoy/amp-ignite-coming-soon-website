import os
import requests
import copy
import json
import traceback

from dotenv import load_dotenv
from django.utils import timezone
from datetime import timedelta

from coming_soon_website.models import ApiToken, ApiTokenRefreshLog, ContactFormData

load_dotenv()

CLIENT_ID = os.getenv("GO_HIGH_LEVEL_CLIENT_ID")
CLIENT_SECRET = os.getenv("GO_HIGH_LEVEL_CLIENT_SECRET")
TOKEN_REFRESH_THRESHOLD_MINUTES = int(os.getenv("TOKEN_REFRESH_THRESHOLD_MINUTES"))

import requests

API_ENDPOINTS = {
    "refresh_access_token": {
        "url": "https://services.leadconnectorhq.com/oauth/token",
        "method": "POST",
        "payload": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
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
    }
}

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
        threshold_time = timezone.now() + timedelta(minutes=TOKEN_REFRESH_THRESHOLD_MINUTES)

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

    refresh_log = ApiTokenRefreshLog(
        api_token=service_token_record
    )

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
            refresh_log.is_refresh_successful = True
            refresh_log.save()
        else:
            print("Request failed, could not refresh access token")
            print(response)
            print(response.text)
            error_log = response.text
            refresh_log.is_refresh_successful = False
            refresh_log.error_log = error_log
            refresh_log.save()
    except Exception as e:
        error_log = "Error: " + str(e) + "\n" + "Traceback:" + traceback.format_exc()
        refresh_log.is_refresh_successful = False
        refresh_log.error_log = error_log
        refresh_log.save()

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
        else:
            print(response.text)
            return False
    except Exception as e:
        print(e)
        return False

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
            if "contact" in json_response and "id" in json_response["contact"]:
                contact_form_data.contact_id = json_response["contact"]["id"]     
            contact_form_data.save()
            return True
        else:
            print(response.text)
            return False
    except Exception as e:
        print(e)
        return False