from typing import Optional

import requests

from weather_forecast import WeatherForecast


# def get_forecast(city: str, state: str, country: Optional[str]) -> WeatherForecast:
def get_forecast(city: str, state: str, country: str | None) -> WeatherForecast:
    country = country or 'US'

    city = city.lower().strip()
    state = state.lower().strip()
    country = country.lower().strip()

    url = 'https://weather.talkpython.fm/api/weather?' \
          f'city={city}&state={state}&country={country}&units=imperial'

    resp = requests.get(url)
    data = resp.json()

    # forecast = {
    #     'temp': data['forecast']['temp'],
    #     'desc': data['weather']['description']
    # }
    forecast = WeatherForecast(data)

    return forecast
