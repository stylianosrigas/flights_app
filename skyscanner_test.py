import requests
import json

#
# url = "http://partners.api.skyscanner.net/apiservices/pricing/v1.0/GB/GBP/en-GB/iata/STN/SKG/2017-05-03/2017-05-05/1?apiKey=sr202365158971473983434381556340"
# # params = "flyFrom=%s&to=%s&dateFrom=%s&dateTo=%s&partner=picky&passengers=1&curr=%s&directFlights=0&locale=GB" \
# #          % (fly_from, fly_to, datetime_from, datetime_to, currency)
# # data = requests.get(url + params).json()['data']
# data = requests.post(url, data={'Content-Type': 'application/x-www-form-urlencoded'})
# print data


from skyscanner.skyscanner import Flights

flights_service = Flights('sr202365158971473983434381556340')
result = flights_service.get_result(
    country='UK',
    currency='GBP',
    locale='en-GB',
    originplace='SIN-sky',
    destinationplace='KUL-sky',
    outbounddate='2017-05-28',
    inbounddate='2017-05-31',
    adults=1).parsed

print(result)