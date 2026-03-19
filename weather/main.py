import asyncio
import os
from dotenv import load_dotenv
from client import WeatherClient, WeatherAPIError

load_dotenv()

async def main():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("API key not found. Please set OPENWEATHER_API_KEY in your .env file.")
        return
    
    async with WeatherClient(api_key=api_key) as weather:
        try:
            city = "Prague"
            res = await weather.get_weather(city)
            temp = res['data']['main']['temp']
            print(f"City: {city} | Temperature: {temp}°C | Source: {res['source']}")
        except WeatherAPIError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
