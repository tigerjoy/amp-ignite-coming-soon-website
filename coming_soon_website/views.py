from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")

def submit_contact_details(request):
    if request.method == 'POST':
        # Get the timezone from the IP address
        ip_address = request.META.get('REMOTE_ADDR')

        return JsonResponse({'ip_address': ip_address, 'message': 'success'})
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

def set_timezone(request):
    if request.method == 'POST' and 'timezone' in request.POST and 'formattedOffset' in request.POST:
        request.session['django_timezone'] = request.POST['timezone'] + " " + request.POST['formattedOffset']
        return JsonResponse({'message': 'Timezone set successfully'})
    elif request.method == 'GET':
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)