from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")

def submit_contact_details(request):
    if request.method == 'POST':
        print(request.POST)
        # Get the timezone from the IP address
        ip_address = request.META.get('REMOTE_ADDR')

        # Get timezone
        timezone = request.session.get('django_timezone', 'UTC')

        return JsonResponse({'ip_address': ip_address, 'timezone': timezone, 'message': 'success'})
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

def set_timezone(request):
    required_attributes = ["timezone", "formattedOffset"]
    all_required_attributes_available = all([attribute in request.POST for attribute in required_attributes])
    if request.method == 'POST' and all_required_attributes_available:
        request.session['django_timezone'] = request.POST['timezone'] + " " + request.POST['formattedOffset']
        return JsonResponse({'message': 'Timezone set successfully'})
    elif request.method == 'GET':
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)