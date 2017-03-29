from urllib2 import Request, urlopen, URLError
import requests
import json
import datetime
from dateutil.relativedelta import relativedelta
from datetime import date

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


def date_prediction(first_arrival_date, first_departure_date, prediction_period_days):
    """
    We need a method that takes the first_arrival_date, the first_departure_date and the prediction_period_months. Calculates the current date and returns a dictionary of all the available datetime_from and datetime_to
     that we will search the prices for.
    :return: 
    """
    weekdays = {
        "0": "Monday",
        "1": "Tuesday",
        "2": "Wednesday",
        "3": "Thursday",
        "4": "Friday",
        "5": "Saturday",
        "6": "Sunday"
    }

    # now = datetime.datetime.now()
    # current_year = now.year
    # current_month = now.month
    # current_day = now.day
    # day_of_the_week = now.weekday()
    # future_date = date.today() + relativedelta(months=+config['prediction_period_months'])
    # future_day = future_date.day
    # future_month = future_date.month
    # future_year = future_date.year
    # print "The period that will be examined is from %s/%s/%s to %s/%s/%s" % (current_day, current_month, current_year, future_day, future_month, future_year)
    # if day_of_the_week < config['arrival_day']:
    #     start_arrival_day = current_day+(config['arrival_day']-day_of_the_week)
    #     if config['arrival_day'] < config['departure_day']:
    #         start_departure_day = start_arrival_day + (config['departure_day']-config['arrival_day'])
    #     else:
    #         print 'The script right supports only prediction inside the same week.'
    # else

    first_arrival_date = date(config['first_arrival_date'][0], config['first_arrival_date'][1],
                              config['first_arrival_date'][2])
    first_departure_date = date(config['first_departure_date'][0], config['first_departure_date'][1],
                                config['first_departure_date'][2])
    div = prediction_period_days / 7
    final_arrival_date = first_arrival_date + datetime.timedelta(days=div * 7)
    final_departure_date = first_departure_date + datetime.timedelta(days=div * 7)

    print "The period that will be examined is from %s to %s" % (first_arrival_date, final_departure_date)
    dates_search = []
    for x in range(0, div+1):
        dates_search.append([(first_arrival_date + datetime.timedelta(days=x * 7)),
                               (first_departure_date + datetime.timedelta(days=x * 7))])

    return dates_search
dates_search = date_prediction(config['first_arrival_date'], config['first_departure_date'], int(config['prediction_period_days']))
# search_flight(config['datetime_from'], config['datetime_to'], config['fly_from'], config['fly_to'], config['currency'])
