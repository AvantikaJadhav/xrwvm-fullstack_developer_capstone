from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"status": "success", "message": "Login successful", "username": username})
        else:
            return JsonResponse({"status": "error", "message": "Invalid credentials"}, status=401)

@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"status": "success", "message": "Logout successful"})