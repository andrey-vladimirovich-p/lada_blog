import requests
from blog.settings import MY_API_KEY


class Weather:
    s_city = "Москва"
    city_id = 524894
    appid = MY_API_KEY
    res = requests.get("http://api.openweathermap.org/data/2.5/weather", params={'id': city_id, 'units': 'metric',
                                                                                 'lang': 'ru', 'APPID': appid})
    data = res.json()
    weat = data['weather'][0]['description']
    temp = data['main']['temp']
    cities = s_city
