# Weather App - Django Project

This is a Django-based Weather App that allows users to sign up, log in, and
search for weather information using a third-party weather API. It includes API
endpoints for user authentication and weather data retrieval.

## Table of Contents

- [Installation](#installation)
- [URLs](#urls)

## Installation

Follow these steps to set up the Weather App on your local machine:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/smrutisahoo31192/weatherapp.git
   cd weatherapp
   ```

2. **Create a virtual environment and activate it:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. **Install project dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up the database:**

check DB setting in settings.py

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
```

```bash
python manage.py migrate
```

5. **Create a superuser (admin) account to manage users and data:**

```bash
python manage.py createsuperuser

deafult:
username - admin
password - admin
```

6. **Add weatherapi key in settings.py:**

```bash
# AccuWeather API Key
ACCUWEATHER_API_KEY = "ABCBCBCBCBBCBCBCBC"
```

7. **Start the development server:**

```bash
python manage.py runserver
```

Access the application in your web browser at http://127.0.0.1:8000/

8. **URLs**

template based URLs:

```bash
Home/Login: ''
Sign Up: 'signup/'
Search: 'search/'
```

API based URLs:

```bash
API Login: '/api/login/'
request_body -
{
    "username": "XYZ",
    "password": "XYZ"
}

API Sign Up: 'api/signup/'
request_body -
{
    "username": "XYZ",
    "password": "XYZ"
}

API Search: 'api/search/'
request_body -
{
    "location": "Delhi"
}
```
