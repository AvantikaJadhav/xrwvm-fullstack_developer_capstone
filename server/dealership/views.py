import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages


def get_dealerships(request):
    state = request.GET.get('state', 'All')
    try:
        if state == 'All':
            response = requests.get('http://localhost:3000/fetchDealers')
        else:
            response = requests.get(f'http://localhost:3000/fetchDealers/{state}')
        dealers = response.json().get('dealers', [])
    except:
        dealers = []
    return render(request, 'index.html', {'dealers': dealers})


def about(request):
    return render(request, 'About.html')


def contact(request):
    return render(request, 'Contact.html')


def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


def logout_request(request):
    logout(request)
    return redirect('index')


def registration_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('psw')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            login(request, user)
            return redirect('index')
    return render(request, 'registration.html')


def get_dealer_reviews(request, dealer_id):
    try:
        response = requests.get(f'http://localhost:3000/fetchReviews/dealer/{dealer_id}')
        reviews = response.json().get('reviews', [])
    except:
        reviews = []
    return render(request, 'dealer_details.html', {'reviews': reviews})


def add_review(request, dealer_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        review_text = request.POST.get('review')
        purchase = request.POST.get('purchase')
        car_make = request.POST.get('car_make')
        car_model = request.POST.get('car_model')
        car_year = request.POST.get('car_year')
        review_data = {
            'name': f'{request.user.first_name} {request.user.last_name}',
            'dealership': dealer_id,
            'review': review_text,
            'purchase': purchase == 'on',
            'car_make': car_make,
            'car_model': car_model,
            'car_year': car_year,
        }
        try:
            requests.post('http://localhost:3000/insertReview', json=review_data)
        except:
            pass
        return redirect('dealer_details', dealer_id=dealer_id)
    return render(request, 'add_review.html', {'dealer_id': dealer_id})


def dealer_details(request, dealer_id):
    dealer = None
    reviews = []
    try:
        dealer_response = requests.get(f'http://localhost:3000/fetchDealer/{dealer_id}')
        dealer = dealer_response.json().get('dealer', {})
        reviews_response = requests.get(f'http://localhost:3000/fetchReviews/dealer/{dealer_id}')
        reviews = reviews_response.json().get('reviews', [])
    except:
        pass
    return render(request, 'dealer_details.html', {'dealer': dealer,'reviews': reviews})