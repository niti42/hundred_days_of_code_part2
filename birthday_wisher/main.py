import datetime as dt
import pandas as pd
import smtplib
from random import randint

MY_EMAIL = "nithishkr62@gmail.com"
PASSWORD = "app_password_gmail"

if __name__ == "__main__":
    today_dt = dt.datetime.now()
    today = (today_dt.month, today_dt.day)
    birthdays = pd.read_csv("birthdays.csv")
    birthdays_dict = {
        (data_row["month"], data_row["day"]): data_row
        for (index, data_row) in birthdays.iterrows()
    }

    if today in birthdays_dict:
        template_num = randint(1, 3)
        with open(f"letter_templates/letter_{template_num}.txt", "r") as file:
            template = file.read()
            template = template.replace("[NAME]", birthdays_dict.get(today)["name"])
            template = template.replace("Angela", "Nithish")

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=birthdays_dict.get(today)["email"],
                                msg=f"Subject:Happy Birthday!!!\n\n{template}")
