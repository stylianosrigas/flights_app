from urllib2 import Request, urlopen, URLError
import requests
import json
import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
import time
import numpy as np
import matplotlib.pyplot as plt
import pylab
import argparse

with open('airlines.json') as data_file:
    airline_json = json.load(data_file)
with open('airports.json') as data_file:
    airports_json = json.load(data_file)

def main(args):
    if args.best_flights_config:
        best_flights_search_builder(args.best_flights_config)
    if args.flight_trends_config:
        flight_trends_search_builder(args.flight_trends_config)


def flight_trends_search_builder(config):
    print 'Start searching for the flight trends in a range of dates for a destination'
    with open(config) as data_file:
        config = json.load(data_file)
    dates_search = date_prediction(config)
    summary = {
        "departure": [],
        "return": []
    }
    for date in dates_search:
        print 'Examining departure for destination - %s for period %s' % (
        config['fly_to'], date[0])
        data = search_flight(config['fly_from'], config['fly_to'], date[0],
                             date[0], config['currency'])
        departure_flight_data = find_cheapest_flight(data, config,
                                                     'departure_flight',
                                                     config['currency'])
        print 'Examining departure for destination - %s for period %s' % (
            config['fly_from'], date[1])
        data = search_flight(config['fly_to'], config['fly_from'], date[1],
                             date[1], config['currency'])
        return_flight_data = find_cheapest_flight(data, config,
                                                  'return_flight',
                                                  config['currency'])

        if departure_flight_data != 'NO FLIGHTS' and return_flight_data != 'NO FLIGHTS':
            summary['departure'].append({"date": date[0], "cost": departure_flight_data['conversion'][config['currency']]})
            summary['return'].append({"date": date[1], "cost": return_flight_data['conversion'][config['currency']]})
    flight_trends_plot_data(summary, config)
    plt.legend()
    plt.show()

def best_flights_search_builder(config):
    print 'Start searching for the best flights in a range of dates and destinations'
    with open(config) as data_file:
        config = json.load(data_file)

    summary = {}
    optimised_summary = {}
    for destination in config['fly_to']:
        summary[destination] = []
        optimised_summary[destination] = {"departure": {"data": "", "date": ""}, "return": {"data": "", "date": ""}}
        dates_search = date_prediction(config)
        departure_cost = 1000000
        return_cost = 1000000
        for date in dates_search:
            print 'Examining departure for destination - %s for period %s' % (destination, date[0])
            data = search_flight(config['fly_from'], destination, date[0],
                                 date[0], config['currency'])
            departure_flight_data = find_cheapest_flight(data, config, 'departure_flight', config['currency'])


            print 'Examining return for destination - %s for period %s' % (destination, date[1])
            data = search_flight(destination, config['fly_from'], date[1],
                                 date[1], config['currency'])
            return_flight_data = find_cheapest_flight(data, config, 'return_flight', config['currency'])


            if departure_flight_data != 'NO FLIGHTS' and return_flight_data != 'NO FLIGHTS':
                if departure_flight_data['conversion'][config['currency']] < departure_cost:
                    best_departure_flight_data = departure_flight_data
                    departure_cost = departure_flight_data['conversion'][config['currency']]
                    best_departure_date = date[0]
                if return_flight_data['conversion'][config['currency']] < return_cost:
                    best_return_flight_data = return_flight_data
                    return_cost = return_flight_data['conversion'][config['currency']]
                    best_return_date = date[1]
                total_cost = departure_flight_data['conversion'][config['currency']] + return_flight_data['conversion'][config['currency']]
                summary[destination].append({'date': (date[0]+'-'+date[1]), 'total_cost': total_cost})

        optimised_summary[destination]['departure']['data'] = best_departure_flight_data
        optimised_summary[destination]['departure']['date'] = best_departure_date
        optimised_summary[destination]['return']['data'] = best_return_flight_data
        optimised_summary[destination]['return']['date'] = best_return_date

        best_flights_plot_data(destination, summary, config)

    with open('detailed_data.json', 'w') as outfile:
        json.dump(summary, outfile)
    create_optimised_data(optimised_summary, config)
    plt.legend()
    plt.show()


def create_optimised_data(optimised_summary, config):

    data = {}
    print optimised_summary
    for destination in optimised_summary:
        destination_data = optimised_summary[destination]
        data[destination] = \
            {
                "departure": [],
                "return": [],
                "total_cost":""
            }
        data[destination]['departure'].append({
            "departure_date": destination_data['departure']['date'],
            "departure_time": time.strftime("%H:%M", time.localtime(destination_data['departure']['data']['dTime'])),
            "arrival_time": time.strftime("%H:%M", time.localtime(destination_data['departure']['data']['aTime'])),
            "departure_airport": destination_data['departure']['data']['flyFrom'],
            "arrival_airport": get_airport_name(destination_data['departure']['data']['flyTo']),
            "airline": "",
            "direct_flight": ""
        })
        data[destination]['return'].append({
            "departure_date": destination_data['return']['date'],
            "departure_time": time.strftime("%H:%M", time.localtime(destination_data['return']['data']['dTime'])),
            "arrival_time": time.strftime("%H:%M", time.localtime(destination_data['return']['data']['aTime'])),
            "departure_airport": destination_data['return']['data']['flyFrom'],
            "arrival_airport": get_airport_name(destination_data['return']['data']['flyTo']),
            "airline": "",
            "direct_flight": ""
        })
        data[destination]['total_cost'] = destination_data['departure']['data']['conversion'][config['currency']] + destination_data['return']['data']['conversion'][config['currency']]
    with open('optimised_data.json', 'w') as outfile:
        json.dump(data, outfile)


def get_airport_name(iata):
    found = False
    for airport in airports_json:
        if airport['iata'] == iata:
            return airport['name']
            found = True
            break
    if found is False:
        return iata



def best_flights_plot_data(destination, summary, config):
    axis_font = {'fontname': 'Arial', 'size': '10'}
    plt.xlabel('Dates', **axis_font)
    plt.ylabel('Total Flight Cost (%s)' % config['currency'], **axis_font)
    x_list = []
    y_list = []
    my_xticks = []
    for i in range(len(summary[destination])):
        x_list.append(i+7)
        y_list.append(summary[destination][i]['total_cost'])
        my_xticks.append(summary[destination][i]['date'])
    x = np.array(x_list)
    y = np.array(y_list)
    plt.xticks(x, my_xticks, size=7, rotation=30)
    plt.title('Scrooge Travel - Best Flights')
    plt.ylim([0, 500])
    plt.plot(x, y, label=destination, ls='--', linewidth=2, marker='o', markersize=6)

def flight_trends_plot_data(summary, config):
    axis_font = {'fontname': 'Arial', 'size': '10'}
    plt.xlabel('Dates', **axis_font)
    plt.ylabel('Total Flight Cost (%s)' % config['currency'], **axis_font)
    x_list = []
    y_list = []
    my_xticks = []
    for i in range(len(summary['departure'])):
        x_list.append(i)
        y_list.append(summary['departure'][i]['cost'])
        my_xticks.append((summary['departure'][i]['date']).split('/')[0])
    x = np.array(x_list)
    y = np.array(y_list)
    plt.xticks(x, my_xticks, size=7, rotation=30)
    plt.title('Scrooge Travel - Flight Trends')
    plt.ylim([0, 500])
    plt.plot(x, y, label='%s - %s' % (config['fly_from'], config['fly_to']), ls='--', linewidth=2, marker='o',
             markersize=6)
    x_list = []
    y_list = []
    my_xticks = []
    for i in range(len(summary['return'])):
        x_list.append(i)
        y_list.append(summary['return'][i]['cost'])
        my_xticks.append((summary['return'][i]['date']).split('/')[0])
    x = np.array(x_list)
    y = np.array(y_list)
    plt.xticks(x, my_xticks, size=7, rotation=30)
    plt.title('Scrooge Travel - Flight Trends')
    plt.ylim([0, 500])
    plt.plot(x, y, label='%s - %s' % (config['fly_to'], config['fly_from']), ls='--', linewidth=2, marker='o',
             markersize=6)


def date_prediction(config):
    """
    We need a method that takes the first_arrival_date, the first_departure_date and the prediction_period_months. Calculates the current date and returns a dictionary of all the available datetime_from and datetime_to
     that we will search the prices for.
    :return:
    """
    if config['functionality'] == 'best_flights':
        departure_flight_date = date(config['departure_flight']['departure_date'][0],
                                  config['departure_flight']['departure_date'][1],
                                  config['departure_flight']['departure_date'][2])
        return_flight_date = date(config['return_flight']['departure_date'][0],
                                    config['return_flight']['departure_date'][1],
                                    config['return_flight']['departure_date'][2])
        div = config['prediction_period_days'] / 7
        dates_search = []
        for x in range(0, div + 1):
            dates_search.append(
                [(departure_flight_date + datetime.timedelta(days=x * 7)),
                 (return_flight_date + datetime.timedelta(days=x * 7))])
        for i in dates_search:
            i[0] = str(i[0])
            year, month, day = i[0].split("-")
            i[0] = "%s/%s/%s" % (day, month, year)
            i[1] = str(i[1])
            year, month, day = i[1].split("-")
            i[1] = "%s/%s/%s" % (day, month, year)
        return dates_search
    elif config['functionality'] == 'flight_trends':
        departure_flight_date = date(
            config['departure_flight']['departure_date'][0],
            config['departure_flight']['departure_date'][1],
            config['departure_flight']['departure_date'][2])
        return_flight_date = date(config['return_flight']['departure_date'][0],
                                  config['return_flight']['departure_date'][1],
                                  config['return_flight']['departure_date'][2])
        dates_search = []
        for x in range(0, config['prediction_period_days']):
            dates_search.append(
                [(departure_flight_date + datetime.timedelta(days=x)),
                 (return_flight_date + datetime.timedelta(days=x))])
        for i in dates_search:
            i[0] = str(i[0])
            year, month, day = i[0].split("-")
            i[0] = "%s/%s/%s" % (day, month, year)
            i[1] = str(i[1])
            year, month, day = i[1].split("-")
            i[1] = "%s/%s/%s" % (day, month, year)
        return dates_search


def search_flight(fly_from, fly_to, datetime_from, datetime_to, currency):
    url = "https://api.skypicker.com/flights?"
    params = "flyFrom=%s&to=%s&dateFrom=%s&dateTo=%s&partner=picky&passengers=1&curr=%s&directFlights=0&locale=GB" \
             % (fly_from, fly_to, datetime_from, datetime_to, currency)
    data = requests.get(url + params).json()['data']
    return data


def find_cheapest_flight(data, config, flight_type, currency):
    cost = 1000000
    flight_check = False
    for entry in data:
        if config[flight_type]['direct_flight'] == 'True':
            if len(entry['route']) == 1:
                departure_time = time.strftime("%H:%M", time.localtime(entry['dTime']))
                arrival_time = time.strftime("%H:%M", time.localtime(entry['aTime']))
                preferred_departure_time = time.strftime(config[flight_type]['departure_time'])
                preferred_arrival_time = time.strftime(config[flight_type]['arrival_time'])
                if (departure_time > preferred_departure_time) and (arrival_time < preferred_arrival_time):
                    flight_check = True
                    if entry['conversion'][currency] < cost:
                        cost = entry['conversion'][currency]
                        best_data = entry
        else:
            if len(entry['route']) == 1:
                departure_time = time.strftime("%H:%M", time.localtime(entry['dTime']))
                arrival_time = time.strftime("%H:%M", time.localtime(entry['aTime']))
                preferred_departure_time = time.strftime(config[flight_type]['departure_time'])
                preferred_arrival_time = time.strftime(config[flight_type]['arrival_time'])
                if (departure_time > preferred_departure_time) and (arrival_time < preferred_arrival_time):
                    flight_check = True
                    if entry['conversion'][currency] < cost:
                        cost = entry['conversion'][currency]
                        best_data = entry
            else:
                departure_time = time.strftime("%H:%M",
                                               time.localtime(entry['dTime']))
                arrival_time = time.strftime("%H:%M",
                                             time.localtime(entry['aTime']))
                preferred_departure_time = time.strftime(
                    config[flight_type]['departure_time'])
                preferred_arrival_time = time.strftime(
                    config[flight_type]['arrival_time'])
                if (departure_time > preferred_departure_time) and (arrival_time < preferred_arrival_time):
                    flight_check = True
                    if entry['conversion'][currency] < cost:
                        cost = entry['conversion'][currency]
                        best_data = entry

    if flight_check == False:
        print '%s - No flight available on this time' % flight_type
        return 'NO FLIGHTS'
    else:
        return best_data



if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Setup elements for the scrooge travel app')
        parser.add_argument("-b", "--best_flights", dest="best_flights_config", metavar='best_flights_config', help='Pash config to check for the best flights in a range of dates and destinations')
        parser.add_argument("-t", "--flight_trends", dest="flight_trends_config", metavar='flight_trends_config', help='Pash config to check for the flight trends')
        args = parser.parse_args()
        main(args)
    except ValueError:
        print "ERROR: Provide one of the available options"
        print traceback.format_exc()
        exit(2)
