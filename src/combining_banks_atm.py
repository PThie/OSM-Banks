# -------------------------------------------------
# import modules

import os
import os.path
import pandas as pd
from helpers.config import config_paths

for tag in ["bank", "atm"]:
    # -------------------------------------------------
    # list files
    
    files = os.listdir(
        os.path.join(
            config_paths().get("data_path"),
            tag
        )    
    )
    
    # ignore archive
    files = [file for file in files if "archive" not in file]


    # -------------------------------------------------
    # read all data
    
    data_storage = list()
    
    for file in files:
        dta = pd.read_csv(
            os.path.join(
                config_paths().get("data_path"),
                tag,
                file
            )    
        )
        
        data_storage.append(dta)
        
    # combine all datasets
    combined_data = pd.concat(data_storage)

    # export
    combined_data.to_csv(
        os.path.join(
            config_paths().get("data_path"),
            tag,
            tag + "_2014_2022.csv"
        ),
        sep = ";"
    )
