""" Config file for bitcoin alert """
import os

# Change in PHP
THRESHOLD = 1000

# How often this bot will check the rates in secs
FREQUENCY = 2400

PUSH_BULLET = {
    'url': 'https://api.pushbullet.com/v2/pushes',
    'token': os.environ['PUSH_BULLET_TOKEN']
}

COINDESK_URL = 'https://api.coindesk.com/v1/bpi/currentprice/php.json'


