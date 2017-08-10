import os.path as opath
import os

dpath = {}
taxi_data_home = opath.join(opath.join(opath.dirname(opath.realpath(__file__)), '..'), 'taxi_data')
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
#
#
# dpath['eeTime'] = opath.join(dpath['home'], 'eeTime')
# dpath['eeTime_ap'] = opath.join(dpath['eeTime'], 'ap')
#
# dpath['qrTimeTerNumber'] = opath.join(dpath['home'], 'qrTimeTerNumber')
# dpath['qrTimeTerNumber_ap'] = opath.join(dpath['qrTimeTerNumber'], 'ap')
# #
dpath['analysis'] = opath.join(dpath['home'], 'analysis')
dpath['pickupAP_Regression'] = opath.join(dpath['analysis'], 'pickupAP_Regression')
dpath['dropoffAP_tTest'] = opath.join(dpath['analysis'], 'dropoffAP_tTest')
dpath['dropoffAP_pickupAP_tTest'] = opath.join(dpath['analysis'], 'dropoffAP_pickupAP_tTest')
dpath['dropoffAP_pickupX_tTest'] = opath.join(dpath['analysis'], 'dropoffAP_pickupX_tTest')





# dpath['1_generalFlow'] = opath.join(dpath['analysis'], '1_generalFlow')
# dpath['2_immediateDecision'] = opath.join(dpath['analysis'], '2_immediateDecision')
# dpath['3_correlation'] = opath.join(dpath['analysis'], '3_correlation')
# dpath['4_hourTrend'] = opath.join(dpath['analysis'], '4_hourTrend')
#
# dpath['6_dropoffRegression'] = opath.join(dpath['analysis'], '6_dropoffRegression')

for dn in [
            'home',
            #
            'log', 'ap_dayLog',
            #
            'trip', 'ap_dayTrip', 'ap_QidQnum',
            #
            #
            #
            # 'eeTime', 'eeTime_ap',
            # 'qrTimeTerNumber', 'qrTimeTerNumber_ap',
            # #
            'analysis',
                'pickupAP_Regression', 'dropoffAP_tTest', 'dropoffAP_pickupAP_tTest', 'dropoffAP_pickupX_tTest'
            #     '1_generalFlow', '2_immediateDecision', '3_correlation', '4_hourTrend',
            #     '6_dropoffRegression',
           ]:
    try:
        if not opath.exists(dpath[dn]):
            os.makedirs(dpath[dn])
    except OSError:
        pass


AM2, AM5 = 2, 5

# For meaningless data filtering
error_hours = [('9', '3', '15', '1'), ('10', '3', '17', '1'), ('10', '7', '4', '6'), ('10', '7', '4', '7'), ('10', '7', '4', '8'),
               # second filtering
                ('10', '3', '17', '6'), ('10', '11', '21', '6'), ('10', '11', '21', '10'),  # Abnormal (long) queueing time
                ('9', '3', '1', '1'), ('9', '11', '8', '1'), ('10', '5', '16', '1'), ('10', '1', '24', '1')  # Abnormal (short) active duration
               ]

MON, TUE, WED, THR, FRI, SAT, SUN = range(7)
DOW = {
    MON : 'MON',
    TUE : 'TUE',
    WED : 'WED',
    THR : 'THR',
    FRI : 'FRI',
    SAT : 'SAT',
    SUN : 'SUN'
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