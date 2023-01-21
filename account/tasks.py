import requests
from datetime import date
from celery import shared_task


@shared_task()
def get_geolocation():
    for i in range(10):
        while True:
            try:
                ip = requests.get("https://api.ipify.org").content.decode("utf8")
            except:
                continue
            break
    geolocation = requests.get(
        f"https://ipgeolocation.abstractapi.com/v1/?api_key=f0973662c4d6488eba98d633f61d18d6&ip_address={ip}"
    )
    geolocation = geolocation.json()
    return geolocation


@shared_task()
def is_holiday():
    geolocation = get_geolocation()
    country_code = geolocation.get("country_code")
    today = date.today()
    holiday = requests.get(
        f"https://holidays.abstractapi.com/v1/?api_key=f0ccc46c46c048a2ba1d80bfb5635211&country={country_code}&year={today.year}&month={today.month}&day={today.day}"
    )
    holiday = holiday.json()
    if len(holiday) == 0:
        return "No holidays"
    print(holiday)
    holiday = holiday[0]
    return holiday.get("name")
