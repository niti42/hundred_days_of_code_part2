import os
from dotenv import load_dotenv


import requests
from pprint import pprint
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

APP_ID = '15ca3619'
NUTRITIONIX_API_KEY = os.getenv('NUTRITIONIX_API_KEY')

GENDER = "male"
WEIGHT_KG = 70
HEIGHT_CM = 178
AGE = 29

nutritionix_exercise_url = 'https://trackapi.nutritionix.com/v2/natural/exercise'
workout_sheet = 'https://api.sheety.co/bb7b4db22c7482feb06a54c51f8e5bf2/myWorkouts/workouts'

nutritionix_headers = {
    "x-app-id": APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
    "Content": "application/json"
}

sheety_headers = {
    "Authorization": os.getenv('SHEETY_AUTHORIZATION_BEARER')
}

exercise_text = input("Tell me which exercises you did: ")
parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
response_nutri = requests.post(url=nutritionix_exercise_url, headers=nutritionix_headers, json=parameters)
result_nutri = response_nutri.json().get('exercises')

for ex in result_nutri:
    current_date_time = datetime.now()
    current_date = current_date_time.strftime("%d/%m/%Y")
    current_time = current_date_time.strftime("%H:%M:%S")

    workout_log = {
        "workout":
            {
                "date": current_date,
                "time": current_time,
                "exercise": ex.get('name'),
                "duration": ex.get('duration_min'),
                "calories": ex.get('nf_calories')

            }

    }
    response_sh = requests.post(url=workout_sheet, json=workout_log, headers=sheety_headers)
    # response_sh= requests.post(url=workout_sheet, json=workout_log,auth=sheety_auth)
    pprint(response_sh.json())
    response_sh.raise_for_status()


