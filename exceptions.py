class WeatherAPIError(Exception):
    """General exception for Weather API errors."""
    pass

class UnauthorizedError(WeatherAPIError):
    """Exception raised for unauthorized access."""
    pass

class CityNotFoundError(WeatherAPIError):
    """Exception raised when the specified city is not found."""
    pass