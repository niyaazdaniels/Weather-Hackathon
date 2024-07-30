from flask import Flask, render_template, request
from weather import main  


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        city = request.form['cityName'] 
        data = fetch_weather_data(city)  
        print("Fetched Weather Data:", data)
    return render_template('index.html', data=data)

def fetch_weather_data(city_name):
    weather_data = main(city_name)
    if weather_data:
        return {
            'name': weather_data.name,
            'current_time': weather_data.current_time,
            'temperature': weather_data.temperature,
            'description': weather_data.description,
            'icon': weather_data.icon,
            'humidity': weather_data.humidity,
            'wind_speed': weather_data.wind_speed,
            'temp_min': weather_data.temp_min,
            'temp_max': weather_data.temp_max,
            'forecast_5_day': weather_data.forecast_5_day,
            'hourly_forecast': weather_data.hourly_forecast,
        }
    else:
        return None  # Handle no weather data


if __name__ == '__main__':
    app.run(debug=True)
