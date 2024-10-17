import glob
import numpy as np
import os

for i in glob.glob('/users/dshutong/.energyflow/datasets/sorted_QG_jets_*.npz')[2:]:
    print("now running:", i)
    
    file_path = "./projects/qgtag/qgtag_config.py"

    print("now reading config.py")
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    lines[4] = "    c.input_path = '"+i+"'\n"
    print("now writing...")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)
    
    print("finish writing")
    os.system("sh run.sh")
    #os.system("sbatch batch.sh")
    #print("begin batch?")

