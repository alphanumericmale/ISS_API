import requests
from datetime import datetime
import smtplib
import time

my_email = "staerckjustin@gmail.com"
lennie = "lennie.peacock@gmail.com"
amy = "amystaerck@gmail.com"
password = "hgmpfsyqtkatlikl"

email_list = [my_email, lennie, amy]

MY_LAT = 51.648800
MY_LON = -0.775950


def get_iss_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")

    response.raise_for_status()

    data = response.json()
    longitude = float(data['iss_position']['longitude'])
    latitude = float(data['iss_position']['latitude'])

    iss_position = (longitude, latitude)

    return iss_position


def is_near():
    iss_pos = get_iss_position()
    if MY_LON + 5 >= iss_pos[0] >= MY_LON - 5:
        if MY_LAT + 5 >= iss_pos[1] >= MY_LAT - 5:
            return True
        else:
            return False
    else:
        return False


def is_dark():
    # formatted=0 gives 24 hour clock
    parameters = dict(lat=MY_LAT, lng=MY_LON, formatted=0)
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    # string parse time
    sunrise = datetime.strptime(data["results"]["sunrise"].split("T")[1].split("+")[0], '%H:%M:%S').time()
    sunset = datetime.strptime(data["results"]["sunset"].split("T")[1].split("+")[0], '%H:%M:%S').time()
    time_now = datetime.now().time()

    if time_now < sunrise or time_now > sunset:
        return True
    else:
        return False


connection = smtplib.SMTP("smtp.gmail.com")
connection.starttls()
connection.login(my_email, password)
connection.sendmail(
    from_addr=my_email,
    to_addrs=my_email,
    msg="Subject:Look up! \n\nThe ISS is above you\n\n  - Justin"
)

while True:
    time.sleep(60)
    if is_dark() and is_near():
        for i in range(len(email_list)):
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(my_email, password)
            connection.sendmail(
                from_addr=email_list[i],
                to_addrs=my_email,
                msg="Subject:Look up!\n\nThe ISS is above you\n\n  - Justin"
            )

# Send email
# run every 60 seconds - then delay for one hour
