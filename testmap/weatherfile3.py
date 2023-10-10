# Corrected weather_icons mapping
def get_weather_icon(description):
    formatted_description = description.lower().replace(" ", "_").replace("-", "_")

    # Check if the exact description exists in the dictionary
    if formatted_description in weather_icons:
        return weather_icons[formatted_description]

    # If the exact description doesn't exist, try some variations
    variations = [
        formatted_description.replace("_", " "),
        formatted_description.replace("_", "-"),
        formatted_description.replace("_", " ").replace("d", ""),
    ]

    for var in variations:
        if var in weather_icons:
            return weather_icons[var]

    return "Icon not found"

# Test the function with example weather descriptions
weather_icons = {
    "clear sky": "assets/01d2x.png",
    "few clouds": "assets/02d@2x.png",
    "scattered clouds": "assets/03d@2x.png",
    "broken clouds": "assets/04d@2x.png",
    "shower rain": "assets/09d@2x.png",
    "rain": "assets/10d@2x.png",
    "thunderstorm": "assets/11d@2x.png",
    "snow": "assets/13d@2x.png",
    "mist": "assets/50d@2x.png",
    "thunderstorm with light rain": "assets/11d@2x.png",
    "thunderstorm with rain": "assets/11d@2x.png",
    "thunderstorm with heavy rain": "assets/11d@2x.png",
    "light thunderstorm": "assets/11d@2x.png",
    "heavy thunderstorm": "assets/11d@2x.png",
    "ragged thunderstorm": "assets/11d@2x.png",
    "thunderstorm with light drizzle": "assets/11d@2x.png",
    "thunderstorm with drizzle": "assets/11d@2x.png",
    "thunderstorm with heavy drizzle": "assets/11d@2x.png",
    "light intensity drizzle": "assets/09d@2x.png",
    "drizzle": "assets/09d@2x.png",
    "heavy intensity drizzle": "assets/09d@2x.png",
    "light intensity drizzle rain": "assets/09d@2x.png",
    "drizzle rain": "assets/09d@2x.png",
    "heavy intensity drizzle rain": "assets/09d@2x.png",
    "shower rain and drizzle": "assets/09d@2x.png",
    "heavy shower rain and drizzle": "assets/09d@2x.png",
    "shower drizzle": "assets/09d@2x.png",
    "light rain": "assets/10d@2x.png",
    "moderate rain": "assets/10d@2x.png",
    "heavy intensity rain": "assets/10d@2x.png",
    "very heavy rain": "assets/10d@2x.png",
    "extreme rain": "assets/10d@2x.png",
    "freezing rain": "assets/10d@2x.png",
    "light intensity shower rain": "assets/10d@2x.png",
    "shower rain": "assets/10d@2x.png",
    "heavy intensity shower rain": "assets/10d@2x.png",
    "ragged shower rain": "assets/10d@2x.png",
    "light snow": "assets/13d@2x.png",
    "snow": "assets/13d@2x.png",
    "heavy snow": "assets/13d@2x.png",
    "sleet": "assets/13d@2x.png",
    "light shower sleet": "assets/13d@2x.png",
    "shower sleet": "assets/13d@2x.png",
    "light rain and snow": "assets/13d@2x.png",
    "rain and snow": "assets/13d@2x.png",
    "light shower snow": "assets/13d@2x.png",
    "shower snow": "assets/13d@2x.png",
    "heavy shower snow": "assets/13d@2x.png"
}


for description in weather_icons:
    icon_path = get_weather_icon(description)
    print(f"Weather description: {description}, Icon path: {icon_path}")