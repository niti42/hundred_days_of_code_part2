import requests
from pprint import pprint

import os
from twilio.rest import Client

OWM_API_KEY = os.environ.get('OWM_API_KEY')
weather_params = {'lat': 16.41,
                  'lon': 131.85,
                  'appid': OWM_API_KEY,
                  'exclude': "current,minutely,daily"
                  }
OWM_ENDPOINT = 'https://api.openweathermap.org/data/2.8/onecall'

ACCOUNT_SID = 'AC8b3eba844325028974886915329a3d33'
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

response = requests.get(OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
data = response.json()

req_forecast = data.get('hourly')[: 12]
weather_12hours = [int(f.get('weather')[0].get('id')) for f in req_forecast]
will_rain = any(wcode < 700 for wcode in weather_12hours)

if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages \
        .create(
        body="It's going to 🌧️ today. Carry your ☂️",
        from_='+14793974417',
        to='+919632728233')
    print(message.status)
