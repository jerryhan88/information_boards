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

hyp_dpath = opath.join(pf_dpath, 'hypothesis')
h1_dpath = opath.join(hyp_dpath, 'h1FlowRatios')
h1data_dpath = opath.join(h1_dpath, '_data')
h1chart_dpath = opath.join(h1_dpath, 'chart')
h2_dpath = opath.join(hyp_dpath, 'h2QNumCV')
h2data_dpath = opath.join(h2_dpath, '_data')


log_dpath = opath.join(pf_dpath, 'log')
flight_dpath = opath.join(pf_dpath, 'flight')
apDF_dpath = opath.join(flight_dpath, 'ap_dayFlight')
apDNF_dpath = opath.join(flight_dpath, 'ap_dayNumFlights')


dir_paths = [data_dpath, geo_dpath, viz_dpath,
             lf_dpath, ef_dpath, pf_dpath,
             #
             log_dpath,
             #
             flight_dpath, apDF_dpath, apDNF_dpath,
             #
             trip_dpath,
             dt_dpath, adt_dpath, aggr_dpath,
             #
             hyp_dpath,
             h1_dpath, h1data_dpath, h1chart_dpath,

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





TH_QRTIME_MAX = 180  # Minute
TH_QRTIME_MIN = 0
TH_PRODUCTIVITY = 80  # Dollar/Hour
TH_DURATION = 1  # Minute


HOUR1 = 3600
HOUR2 = HOUR1 * 2
MIN1 = 60.0
CENT = 100.0
