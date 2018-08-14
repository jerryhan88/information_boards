#!/usr/bin/env bash

#python3 -c "from util_cython import gen_cFile; gen_cFile('_log_extractor')"
#python3 -c "from _log_extractor import run; run('091101', hh='05', taxi_id=6326)" &

#python3 -c "from util_cython import gen_cFile; gen_cFile('a1_log_processing')"
#python3 -c "from a1_log_processing import run; run('0911')" &


python3 -c "from util_cython import gen_cFile; gen_cFile('a2_trip_processing')"
python3 -c "from a2_trip_processing import run; run('0911')" &



#for i in 090{1..9} 0910; do
#    python3 -c "from a1_log_processing import run; run('$i')" &
#    python3 -c "from a2_trip_processing import run; run('$i')" &
#done

#for i in 100{2..9} 10{11..12}; do
#    python3 -c "from a1_log_processing import run; run('$i')" &
#    python3 -c "from a2_trip_processing import run; run('$i')" &
#done

