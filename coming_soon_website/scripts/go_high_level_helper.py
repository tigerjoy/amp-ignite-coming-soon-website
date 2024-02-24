import os
import requests
import copy
import json

from dotenv import load_dotenv
from django.utils import timezone
from datetime import timedelta

from coming_soon_website.models import ApiToken

load_dotenv()

CLIENT_ID = os.getenv("GO_HIGH_LEVEL_CLIENT_ID")
CLIENT_SECRET = os.getenv("GO_HIGH_LEVEL_CLIENT_SECRET")

ENDPOINTS = {
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

    }
}

def is_access_token_valid(service_name):
    service_token_record = ApiToken.objects.filter(service_name=service_name).first()

    if not service_token_record:
        return False
    else:
        # If the token expires in the future
        if timezone.now() < service_token_record.expires_in:
            return True
        else:
            return False

def refresh_access_token(service_name):
    if not service_name:
        print("service_name is invalid")
        return
    
    service_token_record = ApiToken.objects.filter(service_name=service_name).first()

    if not service_token_record:
        print(f"Did not find a service_token_record associated with {service_name}")
        return
    
    request_obj = copy.deepcopy(ENDPOINTS["refresh_access_token"])
    request_obj["payload"]["refresh_token"] = service_token_record.refresh_token

    print(json.dumps(request_obj, indent=4))

    response = requests.post(request_obj["url"], data=request_obj["payload"], headers=request_obj["headers"])

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

