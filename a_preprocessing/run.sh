#!/usr/bin/env bash
#for i in 100{1..9} 10{11..12}; do
for i in 090{1..9} 09{10..11}; do
    python -c "from a5_qrTime_qNumber import run; run('$i')" &
done
