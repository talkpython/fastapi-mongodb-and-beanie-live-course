import asyncio
from typing import Tuple

import httpx


async def main():
    locations = [
        ('Portland', 'OR'),
        ('Seattle', 'WA'),
        ('La Jolla', 'CA'),
        ('Phoenix', 'AZ'),
        ('New York', 'NY'),
        ('Boston', 'MA'),
    ]
    weather_reports = await get_reports(locations)
    for w in weather_reports:
        print(w)
    print("Done.")


async def get_weather(city: str, state: str) -> str:
    url = f'https://weather.talkpython.fm/api/weather?city={city}&state={state}&country=US&units=imperial'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True)
        resp.raise_for_status()

    data = resp.json()
    desc = data['weather']['description']
    temp = data['forecast']['temp']
    weather = f'Weather in {city}, {state} is {desc} and {temp} F'
    return weather


async def get_reports(locations: list[Tuple[str, str]]):
    work = []
    for city, state in locations:
        work.append(asyncio.create_task(get_weather(city, state)))

    # clever version:
    return [await task for task in work]

    # traditional version
    # reports = []
    # for task in work:
    #     reports.append(await task)
    #
    # return reports


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
