import requests
from datetime import datetime
import time
import smtplib
MY_LAT = 51.507351   # Your latitude
MY_LONG = -0.127758  # Your longitude
myemail = "Your Email"
password = 'APP-EMAIL'


def proximity():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    print(iss_latitude, iss_longitude)
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5<=iss_longitude<=MY_LONG+5:
        return True
    return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()
    if time_now.hour <= sunrise or time_now.hour >= sunset:
        return True
    return False


while True:
    time.sleep(60)
    if proximity() == True and is_night() == True:
        with smtplib.SMTP('smtp.gmail.com', 587) as connect:
            # This is to create the connection
            connect.starttls()
            # This method helps to make sure that our connection is safe, it makes our email encrypted
            connect.login(user=myemail, password=password)
            connect.sendmail(from_addr=myemail, to_addrs=myemail, msg=f"Subject:ISS Overhead \n\n Open Your eyes the ISS is above you right now")