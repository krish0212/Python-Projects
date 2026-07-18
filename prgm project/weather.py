import requests
class PublicWeatherApp:    
    def __init__(self):
        self.geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"

    def get_coordinates(self, city_name):
        """Converts a textual city name into Latitude and Longitude coordinates."""
        params = {
            'name': city_name,
            'count': 1,
            'language': 'en'
        }
        try:
            response = requests.get(self.geo_url, params=params)
            response.raise_for_status()
            data = response.json()            
            results = data.get("results")
            if not results:
                print(f" Error: Could not find coordinates for '{city_name}'.")
                return None
                
            city_data = results[0]
            return {
                'lat': city_data.get('latitude'),
                'lon': city_data.get('longitude'),
                'country': city_data.get('country', 'Unknown')
            }
        except requests.exceptions.RequestException as e:
            print(f" Geocoding Network Error: {e}")
            return None

    def get_weather(self, lat, lon):
        """Fetches live weather values using coordinates."""
        params = {
            'latitude': lat,
            'longitude': lon,
            'current_weather': 'true'  
        }
        try:
            response = requests.get(self.weather_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f" Weather API Network Error: {e}")
            return None

    def display_report(self, city_name, geo_info, weather_data):
        if not geo_info or not weather_data:
            return
            
        current = weather_data.get("current_weather", {})
        temp = current.get("temperature")
        windspeed = current.get("windspeed")
        
        print(f"\n=========================================")
        print(f"   WEATHER REPORT: {city_name.upper()}, {geo_info['country']} ")
        print(f"=========================================")
        print(f"  Temperature : {temp}°C")
        print(f"  Wind Speed  : {windspeed} km/h")
        print(f"  Coordinates : {geo_info['lat']}°N, {geo_info['lon']}°E")
        print(f"-----------------------------------------")
        if temp > 30:
            print(" Advice: It's warm outside. Stay hydrated!")
        elif temp < 15:
            print(" Advice: It's chilly. Grab a jacket before you leave!")
        else:
            print(" Advice: The weather is beautiful and pleasant. Enjoy!")
        print(f"=========================================")


if __name__ == "__main__":
    app = PublicWeatherApp()
    user_city = input("Enter city name: ").strip()
    if user_city:
        print(f" Locating '{user_city}'...")
        coords = app.get_coordinates(user_city)
        
        if coords:
            print(" Fetching meteorological readings...")
            raw_weather = app.get_weather(coords['lat'], coords['lon'])
            app.display_report(user_city, coords, raw_weather)
    else:
        print(" Error: Input cannot be left blank.")