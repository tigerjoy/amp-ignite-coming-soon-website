from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

from .models import ContactFormData

from .tasks.go_high_level_tasks import save_contact_flow

# Create your views here.
def home(request):
    return render(request, "home.html")

def submit_contact_details(request):
    required_fields = ["website_type", "form_type", "name", "company", "email", "phone", "customer_message"]
    required_fields_exist = all([attribute in request.POST for attribute in required_fields])

    if request.method == 'POST' and required_fields_exist:
        print(request.POST)
        # Get the timezone from the IP address
        ip_address = request.META.get('REMOTE_ADDR')

        # Get timezone
        timezone = request.session.get('django_timezone', 'UTC')

        form_data = {
            'ip_address': ip_address,
            'timezone': timezone,
            'website_type': request.POST['website_type'],
            'form_type': request.POST['form_type'],
            'name': request.POST['name'],
            'company': request.POST['company'],
            'email': request.POST['email'],
            'phone': request.POST['phone'],
            'customer_message': request.POST['customer_message']
        }

        # Create a ContactFormData object from the dictionary
        contact_data = ContactFormData(**form_data)

        # Save the object to the database
        contact_data.save()

        form_data['message'] = 'success'

        save_contact_flow(contact_data.id, settings.GO_HIGH_LEVEL_SERVICE_NAME, verbose_name=f"save_contact_flow_for_id_{contact_data.id}")

        return JsonResponse(form_data)
    elif request.method == 'GET':
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)

def set_timezone(request):
    required_attributes = ["timezone", "formattedOffset"]
    all_required_attributes_available = all([attribute in request.POST for attribute in required_attributes])
    if request.method == 'POST' and all_required_attributes_available:
        request.session['django_timezone'] = request.POST['timezone']
        return JsonResponse({'message': 'Timezone set successfully'})
    elif request.method == 'GET':
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)