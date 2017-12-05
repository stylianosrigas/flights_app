import json

with open('airports.json') as data_file:
    airports_json = json.load(data_file)

for airport in airports_json:
    if airport['iata'] == 'STN':
        print airport['name']