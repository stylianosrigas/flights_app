from urllib2 import Request, urlopen, URLError
import requests
import json
import datetime

with open('config.json') as data_file:
    config = json.load(data_file)
with open('airlines.json') as data_file:
    airline_json = json.load(data_file)


# request = Request('https://api.skypicker.com/flights?flyFrom=STN&to=SKG&dateFrom=10/04/2017&dateTo=20/05/2017&sort=price&curr=EUR&partner=picky')
#
# response = urlopen(request)
# results = response.read()
# print results


# def airline_name(airline_json, name_check):
#     for i in airline_json:
#         if airline_json['na'] == (name_check.encode('utf-8')):
#             return_value = i['name'].encode('utf-8')
#         else:
#             return_value = 'Error - Airline name not found'
#     return return_value


def search_flight(datetime_from, datetime_to, fly_from, fly_to, currency):
    """Find some cheap flight first
    """
    url = "https://api.skypicker.com/flights?"
    params = "flyFrom=%s&to=%s&dateFrom=%s&dateTo=%s&partner=picky&passengers=1&curr=%s&directFlights=0&locale=GB" \
             % (fly_from, fly_to, datetime_from, datetime_to, currency)
    data = requests.get(url + params).json()['data']
    # for i in data:
    #     if len(i['route']) == 1:
    #         print 'The flight is direct, the cost is %s %s and the airline is - %s' % (i['conversion'][currency], currency, airline_json[i['route'][0]['airline']])

def date_prediction(arrival_day, departure_day, prediction_period_months):
    """
    We need a method that takes the arrival_day, the departure_day and the prediction_period_months. Calculates the current date and returns a list of all the available datetime_from and datetime_to
     that we will search the prices for.
    :return: 
    """
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day
    day_of_the_week=now.weekday()

    print "%s/%s/%s" % (current_day,current_month,current_year)
    print day_of_the_week

date_prediction(config['arrival_day'], config['departure_day'], config['prediction_period_months'])




search_flight(config['datetime_from'], config['datetime_to'], config['fly_from'], config['fly_to'], config['currency'])
