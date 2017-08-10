#! /bin/sh

# 2 common options. You can leave these alone:-
#$ -j y
#$ -cwd
#$ -m e
#$ -M ckhan.2015@phdis.smu.edu.sg
##$ -q "express.q"
##$ -q "short.q"
#$ -q "long.q"


source ~/.bashrc
cd /scratch/ckhan.2015/research/information_boards/b_analysis

#python pickupAP_regression.py $1 $2

#python dropoffAP_pickupAP_tTest.py $1

python dropoffAP_pickupX_tTest.py $1

