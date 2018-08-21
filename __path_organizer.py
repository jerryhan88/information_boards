import os.path as opath
import os
from functools import reduce


TAXI_RAW_DATA_HOME = reduce(opath.join, [opath.expanduser("~"), '..', 'taxi'])


data_dpath = reduce(opath.join, ['..', '_data', 'information_boards'])
geo_dpath = opath.join(data_dpath, 'GeoFiles')
lf_dpath = opath.join(data_dpath, '_logging')
ef_dpath = opath.join(data_dpath, 'ExternalFiles')
pf_dpath = opath.join(data_dpath, 'ProcessedFiles')
viz_dpath = opath.join(data_dpath, 'Viz')
test_dpath = opath.join(data_dpath, 'Test')
#
trip_dpath = opath.join(pf_dpath, 'trip')
dt_dpath = opath.join(trip_dpath, 'dayTrip')
adt_dpath = opath.join(trip_dpath, 'apDayTrip')
aggr_dpath = opath.join(trip_dpath, 'aggrTrip')


log_dpath = opath.join(pf_dpath, 'log')
flight_dpath = opath.join(pf_dpath, 'flight')
apDF_dpath = opath.join(flight_dpath, 'ap_dayFlight')
apDNF_dpath = opath.join(flight_dpath, 'ap_dayNumFlights')


dir_paths = [data_dpath, geo_dpath, viz_dpath,
             lf_dpath, ef_dpath, pf_dpath,
             trip_dpath,
             dt_dpath, adt_dpath, aggr_dpath,


             log_dpath,
             flight_dpath, apDF_dpath, apDNF_dpath,


            test_dpath

             ]


for dpath in dir_paths:
    if opath.exists(dpath):
        continue
    os.mkdir(dpath)




dpath = {}
taxi_data_home = reduce(opath.join, [opath.dirname(opath.realpath(__file__)),
                                     '..',
                                     'taxi_data'])
dpath['raw'] = opath.join(taxi_data_home, 'raw')
dpath['geo'] = opath.join(taxi_data_home, 'geo')
# --------------------------------------------------------------
dpath['home'] = opath.join(taxi_data_home, 'informationBoards')
#
dpath['log'] = opath.join(dpath['home'], 'log')
dpath['ap_dayLog'] = opath.join(dpath['log'], 'ap_dayLog')

dpath['trip'] = opath.join(dpath['home'], 'trip')
dpath['ap_dayTrip'] = opath.join(dpath['trip'], 'ap_dayTrip')
dpath['ap_QidQnum'] = opath.join(dpath['trip'], 'ap_QidQnum')
#
dpath['analysis'] = opath.join(dpath['home'], 'analysis')
dpath['_data'] = opath.join(dpath['analysis'], '_data')
#
dpath['monthTrend'] = opath.join(dpath['analysis'], 'monthTrend')
dpath['monthNTrip'] = opath.join(dpath['monthTrend'], 'monthNTrip')
dpath['monthQTime'] = opath.join(dpath['monthTrend'], 'monthQTime')
dpath['monthQRatio'] = opath.join(dpath['monthTrend'], 'monthQRatio')
#
dpath['hourTrend'] = opath.join(dpath['analysis'], 'hourTrend')
dpath['hourNTrip'] = opath.join(dpath['hourTrend'], 'hourNTrip')
dpath['hourQTime'] = opath.join(dpath['hourTrend'], 'hourQTime')
dpath['hourQRatio'] = opath.join(dpath['hourTrend'], 'hourQRatio')
dpath['hourQNum'] = opath.join(dpath['hourTrend'], 'hourQNum')
dpath['hourProductivity'] = opath.join(dpath['hourTrend'], 'hourProductivity')
#
dpath['hypothesisTest'] = opath.join(dpath['analysis'], 'hypothesisTest')
dpath['hypFRatio'] = opath.join(dpath['hypothesisTest'], 'hypFRatio')
dpath['hypQNumCV'] = opath.join(dpath['hypothesisTest'], 'hypQNumCV')
dpath['hypSCost'] = opath.join(dpath['hypothesisTest'], 'hypSCost')
dpath['hypDScore'] = opath.join(dpath['hypothesisTest'], 'hypDScore')
dpath['hypCorr'] = opath.join(dpath['hypothesisTest'], 'hypCorr')
# dpath['hypCorrNInfl'] = opath.join(dpath['hypothesisTest'], 'hypCorrNInfl')

for dn in [
            'home',
            #
            'log', 'ap_dayLog',
            #
            'trip', 'ap_dayTrip', 'ap_QidQnum',

            'analysis', '_data',
            #
            'monthTrend',
                'monthNTrip', 'monthQTime', 'monthQRatio',
            #
            'hourTrend',
                'hourNTrip', 'hourQTime', 'hourQRatio', 'hourQNum', 'hourProductivity',
            #
            'hypothesisTest',
                'hypFRatio', 'hypQNumCV', 'hypSCost', 'hypDScore', 'hypCorr'
           ]:
    try:
        if not opath.exists(dpath[dn]):
            os.makedirs(dpath[dn])
    except OSError:
        pass




# For meaningless data filtering
error_hours = [('9', '3', '15', '1'), ('10', '3', '17', '1'), ('10', '7', '4', '6'), ('10', '7', '4', '7'), ('10', '7', '4', '8'),
               # second filtering
                ('10', '3', '17', '6'), ('10', '11', '21', '6'), ('10', '11', '21', '10'),  # Abnormal (long) queueing time
                ('9', '3', '1', '1'), ('9', '11', '8', '1'), ('10', '5', '16', '1'), ('10', '1', '24', '1')  # Abnormal (short) active duration
               ]

MON, TUE, WED, THR, FRI, SAT, SUN = range(7)
DOW = {
    MON: 'MON',
    TUE: 'TUE',
    WED: 'WED',
    THR: 'THR',
    FRI: 'FRI',
    SAT: 'SAT',
    SUN: 'SUN'
    }

WEEKENDS = [SAT, SUN]

# Singapore Public Holidays
HOLIDAYS2009 = [
            (2009,1,1),    # New Year's Day, Thursday, 1 January 2009
            (2009,1,26),    # Chinese New Year, Monday, 26 January 2009
            (2009,1,27),    # Chinese New Year, Tuesday, 27 January 2009
            (2009,4,10),    # Good Friday, Friday, 10 April 2009
            (2009,5,1),     # Labour Day, Friday, 1 May 2009
            (2009,5,9),     # Vesak Day, Saturday, 9 May 2009
            (2009,8,10),    # National Day, Sunday*, 9 August 2009
            (2009,9,21),    # Hari Raya Puasa, Sunday*, 20 September 2009
            (2009,11,16),   # Deepavali, Sunday*, 15 November 2009
            (2009,11,27),   # Hari Raya Haji, Friday, 27 November 2009
            (2009,12,25),   # Christmas Day, Friday, 25 December 2009
]
HOLIDAYS2010 = [(2010, 1, 1),  # New Year's Day, Friday, 1 January 2010
            (2010,2,16),  # Chinese New Year, Sunday*, 14 February 2010
            (2010,2,15),  # Chinese New Year, Monday, 15 February 2010
            (2010,4,2),  # Good Friday, Friday, 2 April 2010
            (2010,5,1),  # Labour Day, Saturday, 1 May 2010
            (2010,5,28),  # Vesak Day, Friday, 28 May 2010
            (2010,8,9),  # National Day, Monday, 9 August 2010
            (2010,9,10),  # Hari Raya Puasa, Friday, 10 September 2010
            (2010,11,5),  # Deepavali, Friday, 5 November 2010
            (2010,11,17),  # Hari Raya Haji, Wednesday, 17 November 2010
            (2010,11,17),  # Christmas Day, Saturday, 25 December 2010
]


TH_QRTIME_MAX = 180  # Minute
TH_QRTIME_MIN = 0
TH_PRODUCTIVITY = 80  # Dollar/Hour
TH_DURATION = 1  # Minute


HOUR1 = 3600
HOUR2 = HOUR1 * 2
MIN1 = 60.0
CENT = 100.0



_rgb = lambda r, g, b: (r / float(255), g / float(255), b / float(255))
clists = (
    'blue', 'green', 'red', 'cyan', 'magenta', 'black',
    _rgb(255, 165, 0),  # orange
    _rgb(238, 130, 238),  # violet
    _rgb(255, 228, 225),  # misty rose
    _rgb(127, 255, 212),  # aqua-marine
    'yellow',
    _rgb(220, 220, 220),  # gray
    _rgb(255, 165, 0),  # orange
    'black'
)
mlists = (
    'o',  #    circle
    'v',  #    triangle_down
    '^',  #    triangle_up
    '<',  #    triangle_left
    '>',  #    triangle_right
    's',  #    square
    'p',  #    pentagon
    '*',  #    star
    '+',  #    plus
    'x',  #    x
    'D',  #    diamond
    'h',  #    hexagon1
    '1',  #    tri_down
    '2',  #    tri_up
    '3',  #    tri_left
    '4',  #    tri_right
    '8',  #    octagon
    'H',  #    hexagon2
    'd',  #    thin_diamond
    '|',  #    vline
    '_',  #    hline
    '.',  #    point
    ',',  #    pixel

    'D',  #    diamond
    '8',  #    octagon
    )
FIGSIZE = (8, 6)
terminal_order = ['T1', 'T2', 'T3', 'BudgetT']
