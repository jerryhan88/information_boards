import json

with open('2010010100_6.json') as data_file:
    data = json.load(data_file)
data.keys()
type(data['flightStatuses'][0])
data['flightStatuses'][0].keys()

hours = set()
for flight in data['flightStatuses']:
    _date, _time = flight['arrivalDate']['dateLocal'].split('T')
    _hh, _mm, _ss = _time.split(':')
    hh, mm = map(int, [_hh, _mm])
    ss_sss = float(_ss)
    if hh == 6:
        print('')
        print(flight)
        # assert False
    hours.add(hh)

import requests

s = "https://api.flightstats.com/flex/flightstatus/historical/rest/v3/json/airport/status/SIN/arr/2010/1/1/12?appId=a42321e6&appKey=895a74e02c6c034bf4b642fa0339438a&utc=false&numHours=6"

r = requests.get(s)
r.json()

with open('temp.json', 'w') as f:
    json.dump(r.json(), f)

_date, _time = data['flightStatuses'][0]['arrivalDate']['dateLocal'].split('T')
_hh, _mm, _ss = _time.split(':')
hh, mm = map(int, [_hh, _mm])
ss_sss = float(_ss)

data['flightStatuses'][0]['airportResources']

from datetime import date, timedelta

cur_date = date(2010, 1, 1)
hour_interval = range(0, 24, 6)
while True:
    for hour in hour_interval:
        if (cur_date.year, cur_date.month, cur_date.day, hour) in [(2010, 1, 1, 0), (2010, 1, 1, 6)]:
            continue
        if (cur_date.year, cur_date.month) == (2010, 10):
            continue
        ofpath = '%d%s.json' % (cur_date.year, ''.join('%02d' % x for x in [cur_date.month, cur_date.day, hour]))
        print(ofpath)
        curl = "https://api.flightstats.com/flex/flightstatus/historical/rest/v3/json/airport/status/SIN/arr/%d/%d/%d/%d?appId=a42321e6&appKey=895a74e02c6c034bf4b642fa0339438a&utc=false&numHours=6" % (
        cur_date.year, cur_date.month, cur_date.day, hour)
        print(curl)
        r = requests.get(curl)
        r.json()
        with open(ofpath, 'w') as f:
            json.dump(r.json(), f)
    cur_date += timedelta(days=1)
    if cur_date.year == 2011:
        break

flights, time_flight = set(), set()
for hour in hour_interval:
    ifpath = '%d%s.json' % (2017, ''.join('%02d' % x for x in [7, 7, hour]))
    with open(ifpath) as data_file:
        data = json.load(data_file)
    for flight in data['flightStatuses']:
        flights.add(flight['flightId'])

        _date, _time = flight['arrivalDate']['dateLocal'].split('T')
        _hh, _mm, _ss = _time.split(':')
        hh, mm = map(int, [_hh, _mm])
        time_flight.add((hh, mm, flight['carrierFsCode'], flight['flightNumber']))

map(len, [flights, time_flight])


