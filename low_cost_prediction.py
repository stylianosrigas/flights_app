from urllib2 import Request, urlopen, URLError
import requests
import json
import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
import time

with open('config.json') as data_file:
    config = json.load(data_file)
with open('airlines.json') as data_file:
    airline_json = json.load(data_file)




def search_flight(datetime_from, datetime_to, fly_from, fly_to, currency, check_time, flight_type):
    """Find some cheap flight first
    """
    url = "https://api.skypicker.com/flights?"
    params = "flyFrom=%s&to=%s&dateFrom=%s&dateTo=%s&partner=picky&passengers=1&curr=%s&directFlights=0&locale=GB" \
             % (fly_from, fly_to, datetime_from, datetime_to, currency)
    data = requests.get(url + params).json()['data']
    flight_check = False
    for i in data:
        if len(i['route']) == 1:
            departure_time = time.strftime("%H:%M", time.localtime(i['dTime']))
            arrival_time = time.strftime("%H:%M", time.localtime(i['aTime']))
            cost = 100000
            if departure_time > time.strftime(check_time):
                flight_check = True
                if i['conversion'][currency] < cost:
                    cost = i['conversion'][currency]
                    flight_number = i
    if flight_check == False:
        print '%s - No flight available on this time' % flight_type
    else:
        departure_time = time.strftime("%H:%M", time.localtime(flight_number['dTime']))
        arrival_time = time.strftime("%H:%M", time.localtime(flight_number['aTime']))
        print '%s - The flight is from %s to %s' % (flight_type, flight_number['cityFrom'], flight_number['cityTo'])
        print '%s - The airport is from  %s to %s and the airline %s' % (flight_type, flight_number['flyFrom'], flight_number['flyTo'], airline_json[flight_number['route'][0]['airline']] )
        print '%s - The flight is direct, the cost is %s %s' % (flight_type, flight_number['conversion'][currency], currency)
        print '%s - Departure Time - %s and Arrival Time - %s' % (flight_type, departure_time, arrival_time)



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

    first_arrival_date = date(config['first_arrival_date'][0], config['first_arrival_date'][1],
                              config['first_arrival_date'][2])
    first_departure_date = date(config['first_departure_date'][0], config['first_departure_date'][1],
                                config['first_departure_date'][2])
    div = prediction_period_days / 7
    final_arrival_date = first_arrival_date + datetime.timedelta(days=div * 7)
    final_departure_date = first_departure_date + datetime.timedelta(days=div * 7)

    weekday_arrival = weekdays[str(first_arrival_date.weekday())]
    weekday_departure = weekdays[str(final_departure_date.weekday())]
    print "INFO - The period that I will search for cheap flights is from %s %s to %s %s" % (weekday_arrival, first_arrival_date, weekday_departure, final_departure_date)
    print ''
    dates_search = []
    for x in range(0, div+1):
        dates_search.append([(first_arrival_date + datetime.timedelta(days=x * 7)),
                               (first_departure_date + datetime.timedelta(days=x * 7))])
    for i in dates_search:
        i[0] = str(i[0])
        year, month, day = i[0].split("-")
        i[0] = "%s/%s/%s" % (day, month, year)
        i[1] = str(i[1])
        year, month, day = i[1].split("-")
        i[1] = "%s/%s/%s" % (day, month, year)

    return dates_search

dates_search = date_prediction(config['first_arrival_date'], config['first_departure_date'], config['prediction_period_days'])
for i in dates_search:
    print 'Searching for flights in %s - %s' % (i[0], i[1])
    print '******* DEPARTURE *************'
    search_flight(i[0], i[0], config['fly_from'], config['fly_to'], config['currency'], (config['first_day_departure_time']), 'departure')
    print '******* RETURN *************'
    search_flight(i[1], i[1], config['fly_to'], config['fly_from'], config['currency'], (config['last_day_departure_time']), 'return')
    print ''
    print ''
