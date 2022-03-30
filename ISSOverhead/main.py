import requests
from datetime import datetime
import smtplib

MY_LAT = "your latitude"
MY_LONG = "your longitude"

MY_EMAIL = "your email"
MY_PASSWORD = "your email password"


def iss_overhead():
    if MY_LAT + 5 > iss_latitude or MY_LAT - 5 < iss_latitude:
        if MY_LONG + 5 > iss_longitude or MY_LONG - 5 < iss_latitude:
            return True


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response_sunset_sunrise = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response_sunset_sunrise.raise_for_status()
data_sunset_sunrise = response_sunset_sunrise.json()
sunrise = int(data_sunset_sunrise["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data_sunset_sunrise["results"]["sunset"].split("T")[1].split(":")[0])

response_iss_location = requests.get(url="http://api.open-notify.org/iss-now.json")
response_iss_location.raise_for_status()
data_iss_location = response_iss_location.json()
iss_location = (data_iss_location["iss_position"]["latitude"], data_iss_location["iss_position"]["longitude"])
iss_latitude = float(data_iss_location["iss_position"]["latitude"])
iss_longitude = float(data_iss_location["iss_position"]["longitude"])

now_hour = datetime.now().hour

if now_hour < sunrise or now_hour > sunset:
    iss = iss_overhead()
    if iss:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs="your to email", msg="Subject: Look to the Sky!\n\nThe ISS "
                                                                           "should be overhead right now!")
