#!/bin/bash

#SBATCH -n 4
#SBATCH -N 1
#SBATCH --mem=96G
#SBATCH -t 24:00:00
#SBATCH -p gpu --gres=gpu:1

source ~/anaconda3/etc/profile.d/conda.sh
conda activate poetry

poetry run baler --project qgtag qgtag_project --mode train;poetry run baler --project qgtag qgtag_project --mode compress;poetry run baler --project qgtag qgtag_project --mode decompress;poetry run baler --project qgtag qgtag_project --mode plot
