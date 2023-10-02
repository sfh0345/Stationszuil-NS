import requests

def get_weather_forecast(city):
    API_KEY = "404f6ef44205711ecabaf88bcc8e7c83"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},nl&units=metric&lang=nl&appid={API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return temperature, description
    else:
        print("Fout:", response.status_code)
        return None, None

def main():
    city = input("Voer de stad in (bijv. Amsterdam): ")
    temperature, description = get_weather_forecast(city)

    if temperature is not None and description is not None:
        print("Weersvoorspelling voor", city)
        print("Temperatuur: {} °C".format(temperature))
        print("Beschrijving:", description)
    else:
        print("Kan de weersvoorspelling niet ophalen.")

if __name__ == "__main__":
    main()
