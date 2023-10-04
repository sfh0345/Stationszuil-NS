import requests
from datetime import datetime, timedelta

def get_next_day_forecast(city, hoeveeldagen):
    API_KEY = "404f6ef44205711ecabaf88bcc8e7c83"  # Replace with your OpenWeatherMap API key

    # Get latitude and longitude for the city
    lat, lon = get_city_coordinates(city)

    if lat is None or lon is None:
        print(f"Could not find coordinates for {city}.")
        return None, None

    url = f"http://api.openweathermap.org/data/2.5/onecall?appid={API_KEY}&lat={lat}&lon={lon}&units=metric&lang=nl"

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        # Get the forecast for the next day
        tomorrow = (datetime.now() + timedelta(days=hoeveeldagen)).strftime('%Y-%m-%d')
        for daily_data in weather_data['daily']:
            if datetime.utcfromtimestamp(daily_data['dt']).strftime('%Y-%m-%d') == tomorrow:
                temperature = daily_data['temp']['day']
                description = daily_data['weather'][0]['description']
                return temperature, description
        else:
            return None, None
    else:
        print("Fout:", response.status_code)
        return None, None

def get_city_coordinates(city):
    API_KEY = "404f6ef44205711ecabaf88bcc8e7c83"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        return lat, lon
    else:
        return None, None

# Example usage
city = station

temperature, description = get_next_day_forecast(city, 1)

rounded_temperature = round(temperature, 0)

