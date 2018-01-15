""" Checks bitcoin price every X intervals """

import urllib2
import requests
import json
import config

from datetime import datetime
from time import sleep


def get_data():
    """ Returns bitcoin value """

    headers = {'User-Agent':'Magic Browser'}
    request = urllib2.Request(config.COINDESK_URL, headers=headers)

    try:
        response = urllib2.urlopen(request)
        result = response.read()

        return json.loads(result)
    except urllib2.HTTPError, error:
        print error
    except Exception, error:
        print error


def calc_change(data, prev_data):
    """ Determines if I should buy or sell bitcoins """

    rate = data["bpi"]["PHP"]["rate_float"]
    prev_rate = prev_data["bpi"]["PHP"]["rate_float"]
    message = ''

    if (rate - prev_rate) > config.THRESHOLD:
        if rate > prev_rate:
            message = """\
        Bitcoin has risen from PHP%s to PHP%s. Maybe you should sell!\
            """ % (prev_data["bpi"]["PHP"]["rate"], data["bpi"]["PHP"]["rate"])
        else:
            message = """\
        Bitcoin has dropped from PHP%s to PHP%s. Maybe you should buy!\
            """ % (prev_data["bpi"]["PHP"]["rate"], data["bpi"]["PHP"]["rate"])

        push_notification(message)
    else:
        print 'No change detected @ %s' % datetime.now()
        print 'c:', data["bpi"]["PHP"]["rate"]
        print 'p:', prev_data["bpi"]["PHP"]["rate"]


def push_notification(message):
    """ Sends a push request to all devices """

    if not message:
        return

    data = {
        'type': 'note',
        'title': 'Bitcoin Price Change',
        'body': message
    }

    try:
        headers = {'Access-Token': config.PUSH_BULLET['token']}
        request = requests.post(
            config.PUSH_BULLET['url'],
            headers=headers,
            data=data
        )
        print request.content
    except requests.ConnectionError, error:
        print error
    except Exception, error:
        print error



if __name__ == '__main__':

    C_RATE = P_RATE = get_data()
    while True:
        calc_change(C_RATE, P_RATE)
        P_RATE = C_RATE
        C_RATE = get_data()
        sleep(config.FREQUENCY)

