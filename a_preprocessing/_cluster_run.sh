#! /bin/sh

# 2 common options. You can leave these alone:-
#$ -j y
#$ -cwd
#$ -m e
#$ -M ckhan.2015@phdis.smu.edu.sg
##$ -q "express.q"
##$ -q "short.q"
#$ -q "long.q"


processorID=$1

source ~/.bashrc
cd /scratch/ckhan.2015/information_boards/a_preprocessing

python -c "from a4_ap_enteringExitingTime import run; run($processorID, 64)"
