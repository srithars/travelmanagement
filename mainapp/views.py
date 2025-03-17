from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import *
from django.contrib.auth import logout
import requests


# Create your views here.
def myfunction(request):
    return render(request, "mainpage.html")
def myabout(request):
    return render(request, "about.html")
def myabout1(request):
    return render(request, "about1.html")
def mylogin(request):
    return render(request, "login.html")
def myregistration(request):
    return render(request, "registration.html")
def mycontact(request):
    return render(request, "contact.html")
def mycontact1(request):
    return render(request, "contact1.html")
def adminhome(request):
    return render(request, "adminhomepage.html")
def userhome(request):
    return render(request, "userhomepage.html")

def registration_view(request):
    user_exists = False
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        phone = request.POST['phone']
        if User.objects.filter(email=email).exists():
            messages.info(request, 'User with this email already exists. Please log in.')
            return render(request, 'login.html')
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.save()
        messages.info(request, 'Account created Successfully!')
        return render(request, 'login.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.get(username=username)
        if user.check_password(password):
            # If username and password match, redirect to admin page
            if username == 'admin@gmail.com' and password == 'admin':
                return render(request, 'adminhomepage.html') # Assuming the URL name for the admin page is 'admin_page'
            else:
                return  render(request, 'userhomepage.html')  # Assuming the URL name for the user page is 'user_page'
        else:
            # If password does not match, display a message
            messages.info(request, 'Invalid password. Please try again')
            return render(request, 'login.html')


def show_topplaces(request):
    topplaces = Topplaces.objects.all()
    return render(request, 'show_topplaces.html', {'topplaces': topplaces})

def show_tophotels(request):
    tophotels = Tophotels.objects.all()

    place_query = request.GET.get('place')
    if place_query:
        tophotels = tophotels.filter(place__icontains=place_query)
    return render(request, 'show_tophotels.html', {'tophotels': tophotels})

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('main')

def admin_home(request):
    return render(request, 'adminhomepage.html')

def users_list(request):
    users = User.objects.all()
    return render(request, 'adminhomepage.html', {'users': users})

def places_list(request):
    places = Topplaces.objects.all()
    return render(request, 'adminhomepage.html', {'places': places})

def hotels_list(request):
    hotels = Tophotels.objects.all()
    return render(request, 'adminhomepage.html', {'hotels': hotels})

def get_weather(city):
    api_key = 'your_openweathermap_api_key'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

def weather(request):
    city = request.GET.get('weather')
    if city:
        weather_data = get_weather(city)
        if 'message' in weather_data:
            error_message = weather_data['message']
            return render(request, 'weather.html', {'error': error_message})
        else:
            return render(request, 'weather.html', {'weather_data': weather_data, 'city': city})
    else:
        return render(request, 'weather.html')