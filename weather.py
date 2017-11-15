#! /usr/bin/env python

import argparse
import datetime
import json
import pyowm
import requests

# Constants
HOST = 'https://hooks.slack.com/'
PATH = 'services/T7Y28ACKW/B7Y51QV37/uuzjD3TvMvu588eXunQKvhok'
CHANNEL = '#bring-an-umbrella'


def get_weather():
    """
    Use the pyowm library to check the current forecast for San Francisco, CA
    :return:
        w: weather object
        city: current city
        state current state
    """
    # Set the city and state to get weather information for
    parser = argparse.ArgumentParser(description='Enter City, State')
    parser.add_argument('--city', type=str, help='City that is raining')
    parser.add_argument('--state', type=str, help='State that is raining')
    args = parser.parse_args()
    print('Input city: {}, {}'.format(args.city, args.state))
    city = args.city
    state = args.state

    # API key for OWM
    owm = pyowm.OWM('12610710679d4af701ae5746a1d63c3e')
    
    # Search for current weather in San Francisco, CA
    observation = owm.weather_at_place(city + ',' + state)
    w = observation.get_weather()

    return w, city, state


def post_weather():
    """
    Post weather information in CHANNEL only if status is currently raining
    :return:
        None
    """
    # Build payload and set variables
    payload = {'channel': CHANNEL}
    w, city, state = get_weather()
    status = w.get_status()

    # If the current status is rain then post to the channel the current forecast
    if status == 'Rain':
        curr_time = w.get_reference_time()
        curr_time = datetime.datetime.fromtimestamp(curr_time).strftime('%m/%d/%Y %H:%M')
        high = w.get_temperature('fahrenheit')['temp_max']
        mid = w.get_temperature('fahrenheit')['temp']
        low = w.get_temperature('fahrenheit')['temp_min']
        humidity = w.get_humidity()
        wind_speed = w.get_wind()['speed']
        wind_direction = w.get_wind()['deg']

        # Format the text to be inputted
        text = 'Bring an umbrella! Its currently raining!\nWeather for {}, {} at {}\n    Currently: {}\n    ' \
               'High: {} F\n    Mid: {} F\n    Low: {} F\n    Humidity: {}%\n    Windspeed: {} mph\n    ' \
               'Direction: {} degrees'.format(city, state, curr_time, status, high, mid, low, humidity, wind_speed,
                                              wind_direction)

        # Prepare payload as json data
        payload['text'] = text
        payload = json.dumps(payload)

        # Make request to post message in CHANNEL
        r = requests.post(HOST + PATH, payload)

        if r.text == 'ok':
            print('Message was successfully posted to {}'.format(CHANNEL))
        else:
            print('There was an error: {}'.format(r.text))
    else:
        print('It is not raining, do nothing')


if __name__ == "__main__":
    post_weather()
