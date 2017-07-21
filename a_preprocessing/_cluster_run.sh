#! /bin/sh

# 2 common options. You can leave these alone:-
#$ -j y
#$ -cwd
#$ -m e
#$ -M ckhan.2015@phdis.smu.edu.sg
##$ -q "express.q"
##$ -q "short.q"
#$ -q "long.q"


fn=$1
yy=$2

source ~/.bashrc
cd /scratch/ckhan.2015/research/information_boards/a_preprocessing

python a6_ap_dataArrangement.py fn yy
