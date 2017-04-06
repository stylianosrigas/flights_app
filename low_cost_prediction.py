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
with open('airports.json') as data_file:
    airports_json = json.load(data_file)

weekdays = {
    "0": "Monday",
    "1": "Tuesday",
    "2": "Wednesday",
    "3": "Thursday",
    "4": "Friday",
    "5": "Saturday",
    "6": "Sunday"
}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
                    flight_payload = i
    if flight_check == False:
        # print '%s - No flight available on this time' % flight_type
        pass
    else:
        departure_time = time.strftime("%H:%M", time.localtime(flight_payload['dTime']))
        arrival_time = time.strftime("%H:%M", time.localtime(flight_payload['aTime']))
        # print '%s - The flight is from %s to %s' % (flight_type, flight_payload['cityFrom'], flight_payload['cityTo'])
        # print '%s - The airport is from  %s to %s and the airline %s' % (flight_type, flight_payload['flyFrom'], flight_payload['flyTo'], airline_json[flight_payload['route'][0]['airline']] )
        # print '%s - The flight is direct, the cost is %s %s' % (flight_type, flight_payload['conversion'][currency], currency)
        # print '%s - Departure Time - %s and Arrival Time - %s' % (flight_type, departure_time, arrival_time)
        return flight_payload


def date_prediction(first_arrival_date, first_departure_date, prediction_period_days, weekdays, destination):
    """
    We need a method that takes the first_arrival_date, the first_departure_date and the prediction_period_months. Calculates the current date and returns a dictionary of all the available datetime_from and datetime_to
     that we will search the prices for.
    :return: 
    """

    first_arrival_date = date(config['first_arrival_date'][0], config['first_arrival_date'][1],
                              config['first_arrival_date'][2])
    first_departure_date = date(config['first_departure_date'][0], config['first_departure_date'][1],
                                config['first_departure_date'][2])
    div = prediction_period_days / 7
    final_arrival_date = first_arrival_date + datetime.timedelta(days=div * 7)
    final_departure_date = first_departure_date + datetime.timedelta(days=div * 7)

    weekday_arrival = weekdays[str(first_arrival_date.weekday())]
    weekday_departure = weekdays[str(final_departure_date.weekday())]
    print ''
    print bcolors.OKBLUE + "INFO - The period that I will search for cheap flights in destination - %s is from %s %s to %s %s" % (
    destination, weekday_arrival, first_arrival_date, weekday_departure, final_departure_date) + bcolors.ENDC
    print ''
    dates_search = []
    for x in range(0, div + 1):
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

def print_results(best_zero, best_one, date_zero, date_one):

    print bcolors.HEADER + "---------------------------------------------------------------------------------------------------------------------------" + bcolors.ENDC
    print bcolors.HEADER + "---------------------------------------------------------------------------------------------------------------------------" + bcolors.ENDC
    print "The best dates to fly are %s - %s" % (date_zero, date_one)
    print 'The cheapest flight is from %s to %s and return from %s to %s' % (
        best_zero['cityFrom'], best_zero['cityTo'], best_one['cityFrom'], best_one['cityTo'])
    print 'The airport is from  %s to %s and return from %s to %s' % (
        best_zero['flyFrom'], best_zero['flyTo'], best_one['flyFrom'], best_one['flyTo'])
    if (airline_json[best_zero['route'][0]['airline']] == airline_json[
        best_one['route'][0]['airline']]):
        print "The airline for both flights is %s" % (airline_json[best_zero['route'][0]['airline']])
    else:
        print "The airline is %s and for return %s" % (airline_json[best_zero['route'][0]['airline']],
                                                       airline_json[best_one['route'][0]['airline']])
    print 'The flight is direct and the total cost is %s' % (
        best_zero['conversion'][config['currency']] + best_one['conversion'][config['currency']])
    departure_time_first_flight = time.strftime("%H:%M", time.localtime(best_zero['dTime']))
    arrival_time_first_flight = time.strftime("%H:%M", time.localtime(best_zero['aTime']))
    departure_time_second_flight = time.strftime("%H:%M", time.localtime(best_one['dTime']))
    arrival_time_second_flight = time.strftime("%H:%M", time.localtime(best_one['aTime']))
    print 'Departure and Arrival Times:'
    print "%s-%s" % (departure_time_first_flight, arrival_time_first_flight)
    print "%s-%s" % (departure_time_second_flight, arrival_time_second_flight)
    print bcolors.HEADER + "---------------------------------------------------------------------------------------------------------------------------" + bcolors.ENDC
    print bcolors.HEADER + "---------------------------------------------------------------------------------------------------------------------------" + bcolors.ENDC


def main():
    best_list = []
    for destination in config['fly_to']:
        flight_payload_departure = {}
        flight_payload_return = {}
        for airport in airports_json:
            if airport['iata'] == destination:
                airport_name = airport['name']
        print bcolors.HEADER + "---------------------------------------------------------------------------------------------------------------------------" + bcolors.ENDC
        print bcolors.OKBLUE + 'Searching for cheap flights to %s - %s' % (destination, airport_name) + bcolors.ENDC
        dates_search = date_prediction(config['first_arrival_date'], config['first_departure_date'],
                                       config['prediction_period_days'], weekdays, destination)
        total_cost = 10000
        for i in dates_search:
            print 'Searching for flights in %s - %s' % (i[0], i[1])
            # print '******* DEPARTURE *************'
            flight_payload_depar = search_flight(i[0], i[0], config['fly_from'], destination, config['currency'],
                                                 (config['first_day_departure_time']), 'departure')
            # print '******* RETURN *************'
            flight_payload_ret = search_flight(i[1], i[1], destination, config['fly_from'], config['currency'],
                                               (config['last_day_departure_time']), 'return')
            # print ''
            # print ''
            try:
                if (flight_payload_depar['conversion'][config['currency']] + flight_payload_ret['conversion'][
                    config['currency']]) < total_cost:
                    total_cost = (
                    flight_payload_depar['conversion'][config['currency']] + flight_payload_ret['conversion'][
                        config['currency']])
                    flight_payload_departure = flight_payload_depar
                    flight_payload_return = flight_payload_ret
                    date = i
            except:
                pass
        if not flight_payload_departure or not flight_payload_return:
            print ''
            print bcolors.FAIL + 'No available flight for destination - %s' % destination + bcolors.FAIL
            print ''
            best_list.append('N/A')
        else:
            best_list.append([flight_payload_departure, flight_payload_return])

    for best_option in best_list:
        if best_option is not 'N/A':
            print_results(best_option[0], best_option[1], date[0], date[1])

            # print bcolors.HEADER + "---------------------------------------------------------------------------------------------------------------------------" + bcolors.ENDC
            # print bcolors.HEADER + "---------------------------------------------------------------------------------------------------------------------------" + bcolors.ENDC
            # print "The best dates to fly are %s - %s" % (date[0], date[1])
            # print 'The cheapest flight is from %s to %s and return from %s to %s' % (
            # best_option[0]['cityFrom'], best_option[0]['cityTo'], best_option[1]['cityFrom'], best_option[1]['cityTo'])
            # print 'The airport is from  %s to %s and return from %s to %s' % (
            # best_option[0]['flyFrom'], best_option[0]['flyTo'], best_option[1]['flyFrom'], best_option[1]['flyTo'])
            # if (airline_json[best_option[0]['route'][0]['airline']] == airline_json[
            #     best_option[1]['route'][0]['airline']]):
            #     print "The airline for both flights is %s" % (airline_json[best_option[0]['route'][0]['airline']])
            # else:
            #     print "The airline is %s and for return %s" % (airline_json[best_option[0]['route'][0]['airline']],
            #                                                    airline_json[best_option[1]['route'][0]['airline']])
            # print 'The flight is direct and the total cost is %s' % (
            # best_option[0]['conversion'][config['currency']] + best_option[1]['conversion'][config['currency']])
            # departure_time_first_flight = time.strftime("%H:%M", time.localtime(best_option[0]['dTime']))
            # arrival_time_first_flight = time.strftime("%H:%M", time.localtime(best_option[0]['aTime']))
            # departure_time_second_flight = time.strftime("%H:%M", time.localtime(best_option[1]['dTime']))
            # arrival_time_second_flight = time.strftime("%H:%M", time.localtime(best_option[1]['aTime']))
            # print 'Departure and Arrival Times:'
            # print "%s-%s" % (departure_time_first_flight, arrival_time_first_flight)
            # print "%s-%s" % (departure_time_second_flight, arrival_time_second_flight)
            # print bcolors.HEADER + "---------------------------------------------------------------------------------------------------------------------------" + bcolors.ENDC
            # print bcolors.HEADER + "---------------------------------------------------------------------------------------------------------------------------" + bcolors.ENDC
            #

if __name__ == '__main__':
    main()
