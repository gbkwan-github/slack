# slack
Slack API integration

This a simple python webhook that queries openweathermap.org using a built in python library 'pyown' and posts a message in a given channel if it is currently raining.

## Dependencies
```
python 3.6
pip install pyowm
pip install requests
```

## Example
```
python weather.py --city='Bellingham' --state=WA
```

## Tests
```
gilbert$ python weather.py --city='San Jose' --state=CA
Input city: San Jose, CA
It is not raining, do nothing
gilbert$ python weather.py --city='Bellingham' --state=WA
Input city: Bellingham, WA
Message was successfully posted to #bring-an-umbrella
```

## Run crontab for the specified location to get desired notifications.
This example runs weather updates every day at 7am
```
crontab -e
0 7 * * * ./weather.py --city='Bellingham' --state=WA
0 7 * * * ./weather.py --city='San Francisco' --state=CA
```
