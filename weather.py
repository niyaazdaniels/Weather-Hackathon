# import requests
# from dotenv import load_dotenv
# import os
# from dataclasses import dataclass
# from datetime import datetime, timedelta

# load_dotenv()
# api_key = os.getenv('API_KEY')

# @dataclass
# class WeatherData:
#     main: str 
#     name: str
#     timezone: float
#     description: str
#     icon: str
#     feels_like: int
#     temp_min: int
#     temp_max: int
#     pressure: int
#     humidity: int
#     temperature: int
#     wind_speed: int 
#     sunrise: int      
#     sunset: int
#     current_time: str       

#     # 5 day / 3 hour forecast api
#     # api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}

#     # hourly forecast 
#     # https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={API key}

# def get_lat_lon(city_name, API_key):
#     resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={API_key}').json()
#     # Check if the response contains results
#     if resp:
#         data = resp[0]
#         lat, lon = data.get('lat'), data.get('lon')
#         return lat, lon
#     else:
#         # Return None if no results found
#         return None, None
# def get_current_weather(lat, lon, API_key):
#     if lat is None or lon is None:
#         return None  # Return None if lat or lon is invalid

#     resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()

#     # Check if the weather data is available
#     if resp and 'weather' in resp and len(resp['weather']) > 0:

#         timezone_offset = resp.get('timezone', 0)
#         utc_now = datetime.utcnow()
#         local_time = utc_now + timedelta(seconds=timezone_offset)

#         data = WeatherData(
#             main=resp['weather'][0].get('main'),
#             name=resp.get('name'),
#             timezone=timezone_offset,
#             description=resp['weather'][0].get('description'),
#             icon=resp['weather'][0].get('icon'),
#             feels_like=int(resp['main'].get('feels_like')),
#             temp_min=int(resp['main'].get('temp_min')),
#             temp_max=int(resp['main'].get('temp_max')),
#             pressure=int(resp['main'].get('pressure')),
#             humidity=int(resp['main'].get('humidity')),
#             temperature=int(resp['main'].get('temp')),
#             wind_speed=int(resp['wind'].get('speed', 0)), 
#             sunrise=resp['sys'].get('sunrise'),             
#             sunset=resp['sys'].get('sunset'),
#             current_time=local_time.strftime('%H:%M')                 
#         )
#         return data
#     else:
#         return None  # Return None if weather data is not found

# def main(city_name):
#     if not city_name:  # Check if city name is empty
#         print("No city name entered.")
#         return None
    
#     lat, lon = get_lat_lon(city_name, api_key)
#     weather_data = get_current_weather(lat, lon, api_key)
#     return weather_data

# if __name__ == "__main__":
#     city_name = "Toronto"  # You can test with other city names as needed
#     weather_data = main(city_name)
    
#     if weather_data:
#         print(weather_data)
#     else:
#         print('Weather data not found.')

import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')

@dataclass
class WeatherData:
    main: str 
    name: str
    timezone: float
    description: str
    icon: str
    feels_like: int
    temp_min: int
    temp_max: int
    pressure: int
    humidity: int
    temperature: int  # Changed to int
    wind_speed: float 
    sunrise: int      
    sunset: int
    current_time: str       
    forecast_5_day: list = None
    hourly_forecast: list = None

def get_lat_lon(city_name, API_key):
    try:
        resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={API_key}').json()
        if resp:
            data = resp[0]
            lat, lon = data.get('lat'), data.get('lon')
            return lat, lon
        else:
            return None, None
    except Exception as e:
        print(f"Error retrieving latitude and longitude: {e}")
        return None, None

# today's weather

def get_current_weather(lat, lon, API_key):
    if lat is None or lon is None:
        print("Invalid latitude or longitude.")
        return None

    try:
        # Fetch current weather data
        resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()

        if resp and 'weather' in resp and len(resp['weather']) > 0:
            timezone_offset = resp.get('timezone', 0)
            utc_now = datetime.utcnow()
            local_time = utc_now + timedelta(seconds=timezone_offset)

            data = WeatherData(
                main=resp['weather'][0].get('main'),
                name=resp.get('name'),
                timezone=timezone_offset,
                description=resp['weather'][0].get('description'),
                icon=resp['weather'][0].get('icon'),
                feels_like=int(resp['main'].get('feels_like')),
                temp_min=int(resp['main'].get('temp_min')),
                temp_max=int(resp['main'].get('temp_max')),
                pressure=resp['main'].get('pressure'),
                humidity=resp['main'].get('humidity'),
                temperature=int(resp['main'].get('temp')),  # Changed to int
                wind_speed=resp['wind'].get('speed', 0), 
                sunrise=resp['sys'].get('sunrise'),             
                sunset=resp['sys'].get('sunset'),
                current_time=local_time.strftime('%H:%M')                 
            )

            # Fetch the 5-day forecast
            data.forecast_5_day = get_5_day_forecast(lat, lon, API_key)
            # Fetch the hourly forecast
            data.hourly_forecast = get_hourly_forecast(lat, lon, API_key)

            return data
        else:
            print("Error retrieving current weather data.")
            print(resp)  # Print the entire response for debugging
            return None
    except Exception as e:
        print(f"Error retrieving current weather: {e}")
        return None
    
# 5 Day Forecast

def get_5_day_forecast(lat, lon, API_key):
    try:
        resp = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()
        forecast_dict = {}

        if resp and 'list' in resp:
            for entry in resp['list']:
                date_str = datetime.utcfromtimestamp(entry['dt']).strftime('%Y-%m-%d')

                # Initialize the entry for the date if it doesn't exist
                if date_str not in forecast_dict:
                    forecast_dict[date_str] = {
                        'icon': entry['weather'][0]['icon'],
                        'description': entry['weather'][0]['description'],
                        'temp_max': int(entry['main']['temp_max']),  # Changed to int
                        'temp_min': int(entry['main']['temp_min']),  # Changed to int
                    }
                else:
                    # Update max and min temperatures for that day
                    forecast_dict[date_str]['temp_max'] = max(forecast_dict[date_str]['temp_max'], int(entry['main']['temp_max']))  # Changed to int
                    forecast_dict[date_str]['temp_min'] = min(forecast_dict[date_str]['temp_min'], int(entry['main']['temp_min']))  # Changed to int

        # Convert the dictionary to a list of forecasts
        forecast_list = [
            {
                'date': date,
                'icon': data['icon'],
                'description': data['description'],
                'temp_max': data['temp_max'],
                'temp_min': data['temp_min'],
            }
            for date, data in forecast_dict.items()
        ]

        return forecast_list
    except Exception as e:
        print(f"Error retrieving 5-day forecast: {e}")
        return []

# hourly forecast

def get_hourly_forecast(lat, lon, API_key):
    try:
        resp = requests.get(f'https://api.weatherbit.io/v2.0/forecast/minutely?lat={lat}&lon={lon}&key={API_key}').json()
        hourly_list = []

        if resp and 'data' in resp:
            for entry in resp['data']:
                hourly_list.append({
                    'time': datetime.utcfromtimestamp(entry['timestamp']).strftime('%H:%M'),  # Change to 'timestamp'
                    'icon': entry['weather']['icon'],  # Change to access the weather icon
                    'description': entry['weather']['description'],  # Change to access the weather description
                    'temperature': int(entry['temp']),  # Changed to int
                })
        else:
            print("No hourly forecast data found in response:", resp)  # Debugging line
        
        return hourly_list
    except Exception as e:
        print(f"Error retrieving hourly forecast: {e}")
        return []

def main(city_name):
    if not city_name:
        print("No city name entered.")
        return None
    
    lat, lon = get_lat_lon(city_name, api_key)
    weather_data = get_current_weather(lat, lon, api_key)

    if weather_data:
        weather_data.forecast_5_day = get_5_day_forecast(lat, lon, api_key)
        weather_data.hourly_forecast = get_hourly_forecast(lat, lon, api_key)

    return weather_data

if __name__ == "__main__":
    city_name = "Cape Town"  
    weather_data = main(city_name)
    
    if weather_data:
        print(weather_data)
        print("5 Day Forecast:", weather_data.forecast_5_day)
        print("Hourly Forecast:", weather_data.hourly_forecast)
    else:
        print('Weather data not found.')
