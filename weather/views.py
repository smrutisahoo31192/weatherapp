# weather/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
import requests
from django.shortcuts import render, redirect
from .models import SearchHistory
from django.conf import settings
import json
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.contrib.auth.models import User

# rest_framework
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def api_signup(request):
    """
    This function is used to create a new user using rest_framework
    """
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        try:
            user = User.objects.create_user(username=username, password=password)
        except Exception as e:
            print(e)
            user = None
            return JsonResponse({"error_msg": "User creation Failed"}, status=400)

        if user is not None:
            return JsonResponse(
                {"success_msg": "User created Successfully"}, status=200
            )
        else:
            return JsonResponse({"error_msg": "User creation Failed"}, status=400)
    else:
        return JsonResponse({"error_msg": "Invalid Request"}, status=400)


@csrf_exempt
def api_login(request):
    """
    This function is used to login a user using rest_framework
    """
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)

        # Authenticate the user and login
        if user is not None:
            login(request, user)
            return JsonResponse(
                {"success_msg": "User logged in Successfully"}, status=200
            )
        else:
            return JsonResponse({"error_msg": "User login Failed"}, status=400)


@csrf_exempt
def api_search(request):
    """
    This function is used to search weather data using rest_framework
    """
    if request.method == "POST":
        data = json.loads(request.body)
        location = data.get("location")
        user = request.user

        api_key = settings.ACCUWEATHER_API_KEY

        if api_key:
            # Call the AccuWeather API to get weather data
            weather_data = get_weather_data(location, api_key)

            if weather_data:
                # Store the search history in the database
                weather_data_str = json.dumps(weather_data)
                SearchHistory.objects.create(
                    user=user, location=location, search_details=weather_data_str
                )
                return JsonResponse(
                    {"success_msg": "Search Successful", "data": weather_data},
                    status=200,
                )
            else:
                return JsonResponse({"error_msg": "Search Failed"}, status=400)
        else:
            return JsonResponse({"error_msg": "API key is missing"}, status=400)


def signup(request):
    """
    This function is used to create a new user using django tempaltes
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        # Save the user and login. If the form is invalid, show the form again
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("search")
    else:
        form = UserCreationForm()
    return render(request, "weather/signup.html", {"form": form})


def login_view(request):
    """
    This function is used to login a user using django tempaltes
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("search")
    return render(request, "weather/login.html")


@login_required(login_url="")
def search(request):
    """
    This function is used to search weather data using django tempaltes
    """
    if request.method == "POST":
        location = request.POST["location"]
        user = request.user

        api_key = settings.ACCUWEATHER_API_KEY

        if api_key:
            # Call the AccuWeather API to get weather data
            weather_data = get_weather_data(location, api_key)

            if weather_data:
                # Store the search history in the database
                weather_data_str = json.dumps(weather_data)
                SearchHistory.objects.create(
                    user=user, location=location, search_details=weather_data_str
                )
            else:
                weather_data = None
        else:
            weather_data = None

        return render(request, "weather/search.html", {"weather_data": weather_data})

    return render(request, "weather/search.html", {"weather_data": None})


def get_weather_data(location, api_key):
    """
    This function is used to get weather data from AccuWeather API
    """

    # Call the AccuWeather API to get location key
    url = f"https://dataservice.accuweather.com/locations/v1/search?q={location}&apikey={api_key}"
    response = requests.get(url)

    # If API call is successful, get the location key and call the AccuWeather API again to get weather data
    if response.status_code == 200:
        data = response.json()
        if data:
            location_key = data[0]["Key"]
            url = f"https://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                weather_data = response.json()
                return weather_data[0]
    return None
