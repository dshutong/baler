#!/bin/bash

#SBATCH -n 4
#SBATCH -N 1
#SBATCH --mem=96G
#SBATCH -t 24:00:00
#SBATCH -p gpu --gres=gpu:1

source ~/anaconda3/etc/profile.d/conda.sh
conda activate poetry2

poetry run python baler --project=qgtag --mode=train;poetry run python baler --project=qgtag --mode=compress;poetry run python baler --project=qgtag --mode=decompress;poetry run python baler --project=qgtag --mode=info;poetry run python baler --project=qgtag --mode=plot


