#!/usr/bin/env bash

python3 -c "from a1_log_processing import run; run('0911')" &
#python3 -c "from a2_trip_processing import run; run('1001')" &



#for i in 090{1..9} 09{10..11}; do
#    python -c "from a4_ap_dayTrip import run; run('$i')" &
#    python -c "from a5_ap_QidQNum import run; run('$i')" &
#done

#for i in 100{1..9} 10{11..12}; do
#    python -c "from a4_ap_dayTrip import run; run('$i')" &
#    python -c "from a5_ap_QidQNum import run; run('$i')" &
#done



#for i in 090{1..9} 09{10..11}; do
#for i in 100{1..9} 10{11..12}; do
#    python -c "from a5_ap_qrTimeTerNumber import run; run('$i')" &
#done


#python -c "from a5_ap_qrTimeTerNumber import filtering; filtering('09')" &
#python -c "from a5_ap_qrTimeTerNumber import filtering; filtering('10')" &

#python -c "from a6_ap_ecoProfit import run; run('09')" &
#python -c "from a6_ap_ecoProfit import run; run('10')" &
