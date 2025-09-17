from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Contact
import json
import re

def home(request):
    return render(request,'index.html')

@csrf_exempt
def contact_submit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            message = data.get('message', '').strip()

            if not re.match(r'^[a-zA-Z\s]{3,}$', name):
                return JsonResponse({'success': False,'message':'Name must be at least 3 characters and contain only letters'}, status=400)
            
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                return JsonResponse({'success': False,'message':'Please enter a valid email address'}, status=400)
            
            if len(message) < 10:
                return JsonResponse({'success': False,'message':'Message must be at least 10 characters long'}, status=400)
            
            contact = Contact(name=name,email=email,message=message)
            contact.save()
            
            return JsonResponse({'success': True,'message': 'Message sent successfully!'})
            
        except Exception as e:
            return JsonResponse({'success': False,'message': 'Something went wrong. Please try again.'}, status=500)
    
    return JsonResponse({'success': False,'message': 'Invalid request'}, status=405)