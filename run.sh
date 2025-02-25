#!/bin/bash

source ~/anaconda3/etc/profile.d/conda.sh
conda activate poetry

poetry run baler --project qgtag qgtag_project --mode train;poetry run baler --project qgtag qgtag_project --mode compress;poetry run baler --project qgtag qgtag_project --mode decompress;poetry run baler --project qgtag qgtag_project --mode plot
