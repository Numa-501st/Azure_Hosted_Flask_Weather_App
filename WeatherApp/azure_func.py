import logging
import requests
import os
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    city = "London"

    weather_data = get_weather_data(city)

    if weather_data:
        temperature = weather_data['main']['temp'] - 273.15  
        condition = weather_data['weather'][0]['description']

        # Check the conditions
        if temperature < 0 or temperature > 27 or "rain" in condition.lower() or "snow" in condition.lower():
            send_alert(city, temperature, condition)

    return func.HttpResponse(f"Weather alert check completed for {city}.")

def get_weather_data(city):
    weather_api_url = "http://api.openweathermap.org/data/2.5/weather" 
    api_key = os.getenv("WEATHER_API_KEY")  
    response = requests.get(f"{weather_api_url}?q={city}&APPID={api_key}")
    data = response.json()

    if data['cod'] == 200:
        return data
    else:
        logging.error(f"Error fetching weather data: {data.get('message')}")
        return None

def send_alert(city, temperature, condition):
    alert_message = f"Weather alert for {city}! Current temperature is {temperature:.2f}°C with condition: {condition}"
    logging.info(alert_message)

    logic_app_url = os.getenv("LOGIC_APP_URL")  # store logic app url in an env vaiable
    payload = {
        "city": city,
        "temperature": temperature,
        "condition": condition
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(logic_app_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        logging.info(f"Alert sent successfully: {alert_message}")
    else:
        logging.error(f"Failed to send alert: {response.status_code} - {response.text}")
