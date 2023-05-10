import requests
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2, degrees
import smtplib
import time

MY_LAT = 13.033490438035138  # Your latitude
MY_LONG = 77.68738593944845  # Your longitude

MY_EMAIL = "nithishkr62@gmail.com"
PASSWORD = "app_password_gmail"


def haversine(lat1, lon1, lat2, lon2):
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) * sin(dlon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return degrees(c)


def is_iss_close_to_me(my_lat, my_long, iss_lat, iss_long):
    print(my_lat, my_long, iss_lat, iss_long)
    distance = haversine(my_lat, my_long, iss_lat, iss_long)
    print(distance)
    return distance <= 5


def is_dark(sunrise_time, sunset_time):
    time_now = datetime.now()
    present_hour = time_now.time().hour
    return (present_hour >= sunset_time) or (present_hour < sunrise_time)


def send_email_alert():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"Subject:ISS Overhead!!!\n\nThe International space "
                                f"station can now be spotted. Head out to watch it in the sky!!")


def iss_overhead_alert(iss_lat, iss_long):
    if is_iss_close_to_me(MY_LAT, MY_LONG, iss_lat, iss_long):
        send_email_alert()


def get_iss_lat_long():
    response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data_iss = response_iss.json()

    latitude = float(data_iss["iss_position"]["latitude"])
    longitude = float(data_iss["iss_position"]["longitude"])

    return latitude, longitude


def get_sunrise_sunset_times(my_lat, my_long):
    parameters = {
        "lat": my_lat,
        "lng": my_long,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise_time = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_time = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    return sunrise_time, sunset_time


if __name__ == "__main__":
    while True:
        time.sleep(60)
        sunrise, sunset = get_sunrise_sunset_times(MY_LAT, MY_LONG)
        iss_latitude, iss_longitude = get_iss_lat_long()
        if is_dark(sunrise, sunset) and is_iss_close_to_me(MY_LAT, MY_LONG, iss_latitude, iss_longitude):
            send_email_alert()
            print("email alert sent")
