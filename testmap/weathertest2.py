import requests
import datetime
from datetime import datetime, timedelta
import random


list_stations = ["Arnhem", "Almere", "Amersfoort", "Almelo", "Alkmaar", "Apeldoorn", "Assen", "Amsterdam", "Boxtel", "Breda", "Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag", "Hengelo", "Haarlem", "Helmond", "Hoorn", "Heerlen", "Den Bosch", "Hilversum", "Leiden", "Lelystad", "Leeuwarden", "Maastricht", "Nijmegen", "Oss", "Roermond", "Roosendaal", "Sittard", "Tilburg", "Utrecht", "Venlo", "Vlissingen", "Zaandam", "Zwolle", "Zutphen"]
station = random.choice(list_stations)
city = station

#alle mogelijke descriptions aan een image gekoppeld....
weather_icons = {
    "assets/01d2x.png": "clear sky",
    "assets/02d@2x.png": "few clouds",
    "assets/03d@2x.png": "scattered clouds",
    "assets/04d@2x.png": "broken clouds",
    "assets/09d@2x.png": "shower rain",
    "assets/10d@2x.png": "rain",
    "assets/11d@2x.png": "thunderstorm",
    "assets/13d@2x.png": "snow",
    "assets/50d@2x.png": "mist",
    # Group 2xx: Thunderstorm
    "assets/11d@2x.png": "thunderstorm with light rain",
    "assets/11d@2x.png": "thunderstorm with rain",
    "assets/11d@2x.png": "thunderstorm with heavy rain",
    "assets/11d@2x.png": "light thunderstorm",
    "assets/11d@2x.png": "thunderstorm",
    "assets/11d@2x.png": "heavy thunderstorm",
    "assets/11d@2x.png": "ragged thunderstorm",
    "assets/11d@2x.png": "thunderstorm with light drizzle",
    "assets/11d@2x.png": "thunderstorm with drizzle",
    "assets/11d@2x.png": "thunderstorm with heavy drizzle",
    # Group 3xx: Drizzle
    "assets/09d@2x.png": "light intensity drizzle",
    "assets/09d@2x.png": "drizzle",
    "assets/09d@2x.png": "heavy intensity drizzle",
    "assets/09d@2x.png": "light intensity drizzle rain",
    "assets/09d@2x.png": "drizzle rain",
    "assets/09d@2x.png": "heavy intensity drizzle rain",
    "assets/09d@2x.png": "shower rain and drizzle",
    "assets/09d@2x.png": "heavy shower rain and drizzle",
    "assets/09d@2x.png": "shower drizzle",
    # Group 5xx: Rain
    "assets/10d@2x.png": "light rain",
    "assets/10d@2x.png": "moderate rain",
    "assets/10d@2x.png": "heavy intensity rain",
    "assets/10d@2x.png": "very heavy rain",
    "assets/10d@2x.png": "extreme rain",
    "assets/10d@2x.png": "freezing rain",
    "assets/10d@2x.png": "light intensity shower rain",
    "assets/10d@2x.png": "shower rain",
    "assets/10d@2x.png": "heavy intensity shower rain",
    "assets/10d@2x.png": "ragged shower rain",
    # Group 6xx: Snow
    "assets/13d@2x.png": "light snow",
    "assets/13d@2x.png": "snow",
    "assets/13d@2x.png": "heavy snow",
    "assets/13d@2x.png": "sleet",
    "assets/13d@2x.png": "light shower sleet",
    "assets/13d@2x.png": "shower sleet",
    "assets/13d@2x.png": "light rain and snow",
    "assets/13d@2x.png": "rain and snow",
    "assets/13d@2x.png": "light shower snow",
    "assets/13d@2x.png": "shower snow",
    "assets/13d@2x.png": "heavy shower snow",
    # Group 7xx: Atmosphere
    "assets/50d@2x.png": "mist",
    "assets/50d@2x.png": "smoke",
    "assets/50d@2x.png": "haze",
    "assets/50d@2x.png": "sand/dust whirls",
    "assets/50d@2x.png": "fog",
    "assets/50d@2x.png": "sand",
    "assets/50d@2x.png": "dust",
    "assets/50d@2x.png": "volcanic ash",
    "assets/50d@2x.png": "squalls",
    "assets/50d@2x.png": "tornado",
    # Group 800: Clear
    "assets/01d2x.png": "clear sky",
    # Group 80x: Clouds
    "assets/02d@2x.png": "few clouds",
    "assets/03d@2x.png": "scattered clouds",
    "assets/04d@2x.png": "broken clouds",
    "assets/04d@2x.png": "overcast clouds"
}


def get_next_day_forecast(city, hoeveeldagen):
    API_KEY = "404f6ef44205711ecabaf88bcc8e7c83"  # Replace with your OpenWeatherMap API key

    # Get latitude and longitude for the city
    lat, lon = get_city_coordinates(city)

    if lat is None or lon is None:
        print(f"Could not find coordinates for {city}.")
        return None, None

    url = f"http://api.openweathermap.org/data/2.5/onecall?appid={API_KEY}&lat={lat}&lon={lon}&units=metric&lang=eng"

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
def construct_api_argument():
    # Constructing the main argument for the API with "main" instead of "description"
    api_argument = {
        "main": weather_icons
    }
    return json.dumps(api_argument)
def get_weather_icon(description):
    # Directly fetch the icon based on the description
    return weather_icons.get(description, "No corresponding weather icon found.")


temperature, description = get_next_day_forecast(city, 0)
temperature1, description1 = get_next_day_forecast(city, 1)
temperature2, description2 = get_next_day_forecast(city, 2)
temperature3, description3 = get_next_day_forecast(city, 3)

rounded_temperature = round(temperature, 0)
rounded_temperature1 = round(temperature1, 0)
rounded_temperature2 = round(temperature2, 0)
rounded_temperature3 = round(temperature3, 0)

(get_next_day_forecast(city, 0))
(get_next_day_forecast(city, 1))
(get_next_day_forecast(city, 2))
(get_next_day_forecast(city, 3))


icon = get_weather_icon(description)
icon1 = get_weather_icon(description1)
icon2 = get_weather_icon(description2)
icon3 = get_weather_icon(description3)




print(f"Icon for description: {icon}")
print(f"Icon for description1: {icon1}")
print(f"Icon for description2: {icon2}")
print(f"Icon for description3: {icon3}")