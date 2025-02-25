import glob
import numpy as np
import os

for i in glob.glob('/users/dshutong/.energyflow/datasets/QG_jets_*.npz'):
    print("now running:", i)
    
    file_path = "./workspaces/qgtag/qgtag_project/config/qgtag_project_config.py"

    print("now reading config.py")
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    lines[4] = "    c.input_path = '"+i+"'\n"
    print("now writing...")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)
    
    print("finish writing")
    os.system("sh run.sh")
