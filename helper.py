import json


with open('airlines_helper.json') as data_file:
    airline_json = json.load(data_file)


for i in airline_json:
    print '"%s":"%s",' % (i['iata'], i['name'])
