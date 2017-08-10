#!/usr/bin/env bash

#dropoffAP_dataProcess pickupAP_dataProcess

#for fn in no_fixed dow_fixed hour_fixed month_fixed driver_fixed month_driver_fixed; do
#    for dv in durTillPickup productivity ecoProfit; do
#        qsub _cluster_run.sh $fn $dv
#    done
#done


#for fn in no_fixed dow_fixed hour_fixed month_fixed driver_fixed month_driver_fixed; do
#    qsub _cluster_run.sh $fn $dv
#done


for fe_flag in wh; do
    for m_flag in Q I P; do
        qsub _cluster_run.sh $fe_flag $m_flag
    done
done