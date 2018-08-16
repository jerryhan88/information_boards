#!/usr/bin/env bash

#python3 -c "from util_cython import gen_cFile; gen_cFile('_log_extractor')"
#python3 -c "from _log_extractor import run; run('091101', hh='05', taxi_id=6326)" &

python3 -c "from util_cython import gen_cFile; gen_cFile('a1_log_processing')"
python3 -c "from a1_log_processing import run; run('1004')" &


#python3 -c "from util_cython import gen_cFile; gen_cFile('a2_trip_processing')"
#python3 -c "from a2_trip_processing import run; run('1003')" &


#python3 -c "from util_cython import gen_cFile; gen_cFile('a3_dayTrip')"
#python3 -c "from a3_dayTrip import run; run('1002')" &

#python3 -c "from util_cython import gen_cFile; gen_cFile('a4_apDayTrip')"
#python3 -c "from a4_apDayTrip import run; run('-200911')" &
#python3 -c "from a4_apDayTrip import run; run('-201001')" &

