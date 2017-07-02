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
dpath['log_ap'] = opath.join(dpath['log'], 'ap')

dpath['trip'] = opath.join(dpath['home'], 'trip')
dpath['trip_ap'] = opath.join(dpath['trip'], 'ap')

dpath['eeTime'] = opath.join(dpath['home'], 'eeTime')
dpath['eeTime_ap'] = opath.join(dpath['eeTime'], 'ap')
#
dpath['qrTimeTerNumber'] = opath.join(dpath['home'], 'qrTimeTerNumber')
dpath['qrTimeTerNumber_ap'] = opath.join(dpath['qrTimeTerNumber'], 'ap')



for dn in ['home',
           'log', 'log_ap',
           'trip', 'trip_ap',
           'eeTime', 'eeTime_ap',
           'qrTimeTerNumber', 'qrTimeTerNumber_ap',
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