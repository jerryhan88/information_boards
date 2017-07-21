#!/usr/bin/env bash

#dropoffAP_dataProcess pickupAP_dataProcess

for fn in basicProcess; do
    for yy in 09 10; do
        qsub _cluster_run.sh $fn $yy
    done
done