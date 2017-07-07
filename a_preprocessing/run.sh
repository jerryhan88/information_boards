#!/usr/bin/env bash

#for i in 090{1..9} 09{10..11}; do
#    python -c "from a3_ap_tripLocation_prevTripEndTime import run; run('$i')" &
#done

for i in 090{1..9} 09{10..11}; do
#for i in 100{1..9} 10{11..12}; do
    python -c "from a5_ap_qrTimeTerNumber import run; run('$i')" &
done


#python -c "from a5_ap_qrTimeTerNumber import filtering; filtering('09')" &
#python -c "from a5_ap_qrTimeTerNumber import filtering; filtering('10')" &
