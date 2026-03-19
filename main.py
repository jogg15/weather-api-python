import asyncio
import os
from client import WeatherClient, WeatherAPIError

async def main():
    API_KEY = "555544f8eca6da67954076a7801d42d2"

    async with WeatherClient(api_key=API_KEY, cache_ttl=300) as weather:
        try:
            result = await weather.get_weather("Prague")
            temp = result['data']['main']['temp']
            print(f"Teplota v Praze: {temp}°C (Zdroj: {result['source']})")

            result_cached = await weather.get_weather("Prague")
            print(f"Teplota v Praze: {temp}°C (Zdroj: {result_cached['source']})")

        except WeatherAPIError as e:
            print(f"Chyba: {e}")

if __name__ == "__main__":
    asyncio.run(main())    