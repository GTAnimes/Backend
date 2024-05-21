from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if not (username and password):
            return JsonResponse({'error': 'Username and password are required.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=400)
        
        user = User(username=username)
        user.set_password(password)
        user.save()
        
        return JsonResponse({'message': 'User created successfully.'}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if not (username and password):
            return JsonResponse({'error': 'Username and password are required.'}, status=400)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Username does not exist.'}, status=400)
        
        if not user.check_password(password):
            return JsonResponse({'error': 'Incorrect password.'}, status=400)
        
        user_data = {
            'id': user.id,
            'username': user.username,
            # Include other fields as needed
        }
        
        return JsonResponse({'message': 'User logged in successfully.', 'data': user_data}, status=200)

    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
    