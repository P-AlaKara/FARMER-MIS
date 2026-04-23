import requests
from django.conf import settings


CROP_INSIGHTS = {
    'maize': {
        'optimal_temp': (18, 30),
        'rain_tip': 'Maize needs consistent moisture irrigate if no rain in 7 days.',
        'hot_tip': 'High temps can cause heat stress on maize. Water early morning.',
        'cold_tip': 'Maize is frost-sensitive. Protect seedlings if temps drop below 10°C.',
    },
    'sorghum': {
        'optimal_temp': (12, 25),
        'rain_tip': 'Sorghum prefers moderate moisture. Avoid waterlogging.',
        'hot_tip': 'Heat above 25°C during grain fill can reduce sorghum yield.',
        'cold_tip': 'Sorghum can tolerate cold, but young plants need protection.',
    },
    'tomato': {
        'optimal_temp': (18, 27),
        'rain_tip': 'Tomatoes need even watering. Heavy rain can cause blossom drop.',
        'hot_tip': 'Above 35°C, tomato pollen becomes sterile. Use shade cloth.',
        'cold_tip': 'Temperatures below 10°C slow tomato growth.',
    },
}

# Default insights when specific crop is unknown
DEFAULT_INSIGHT = {
    'optimal_temp': (15, 30),
    'rain_tip': 'Ensure your crop has adequate moisture.',
    'hot_tip': 'High temperatures detected, increase watering frequency.',
    'cold_tip': 'Cool temperatures detected, monitor for frost and protect sensitive crops.',
}


def get_weather(city: str) -> dict | None:
    """Fetch current weather from OpenWeatherMap."""
    api_key = settings.OPENWEATHER_API_KEY
    if not api_key or not city:
        return None
    try:
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'appid': api_key, 'units': 'metric'}
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
        }
    except Exception:
        return None


def get_farming_insight(weather: dict, crop: str) -> str:
    """Simple rule-based farming insight."""
    if not weather:
        return 'Weather data unavailable. Check your city setting to get personalized insights.'

    crop_key = crop.lower() if crop else ''
    rules = CROP_INSIGHTS.get(crop_key, DEFAULT_INSIGHT)
    temp = weather['temperature']
    humidity = weather['humidity']
    low, high = rules['optimal_temp']

    insights = []

    if temp > high:
        insights.append(rules['hot_tip'])
    elif temp < low:
        insights.append(rules['cold_tip'])
    else:
        insights.append(f'Temperature ({temp}°C) is in the optimal range for your crop. Good growing conditions today.')

    if humidity > 80:
        insights.append('High humidity detected — watch for fungal diseases. Ensure good airflow around plants.')
    elif humidity < 30:
        insights.append('Low humidity — increase irrigation and consider mulching to retain soil moisture.')

    return ' '.join(insights)