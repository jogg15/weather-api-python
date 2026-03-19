import aiohttp
import time
from typing import Dict, Optional, Any
from exceptions import WeatherAPIError, UnauthorizedError, CityNotFoundError

class WeatherClient:
    def __init__(self, api_key: str, cache_ttl: int = 600):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, tuple[float, Dict[str, Any]]] = {}
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    async def get_weather(self, city: str, units: str = "metric") -> Dict[str, Any]:
        cache_key = f"{city.lower()}_{units}"
        
        if cache_key in self._cache:
            timestamp, data = self._cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return {"data": data, "source": "cache"}

        params = {
            "q": city,
            "appid": self.api_key,
            "units": units
        }

        try:
            async with self._session.get(self.base_url, params=params) as response:
                if response.status == 401:
                    raise UnauthorizedError("Invalid API Key.")
                if response.status == 404:
                    raise CityNotFoundError(f"City '{city}' not found.")
                if response.status != 200:
                    raise WeatherAPIError(f"API Error: {response.status}")

                data = await response.json()
                self._cache[cache_key] = (time.time(), data)
                return {"data": data, "source": "api"}
                
        except aiohttp.ClientError as e:
            raise WeatherAPIError(f"Connection failed: {e}")
