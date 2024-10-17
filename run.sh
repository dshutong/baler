#!/bin/bash

source ~/anaconda3/etc/profile.d/conda.sh
conda activate poetry2

poetry run python baler --project=qgtag --mode=train;poetry run python baler --project=qgtag --mode=compress;poetry run python baler --project=qgtag --mode=decompress;poetry run python baler --project=qgtag --mode=info;poetry run python baler --project=qgtag --mode=plot
