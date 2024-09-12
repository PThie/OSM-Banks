# -------------------------------------------------
# import modules

import os
import osmnx
import pandas as pd
from helpers.config import config_paths

#--------------------------------------------------
# set up

# define tags
user_tags = ["bank", "atm"]

# folder structure (creates folders for storage)
for user_tag in user_tags:
    is_exist = os.path.exists(
        os.path.join(
            config_paths().get("data_path"),
            user_tag
        )
    )

    if not is_exist:
        os.makedirs(
            os.path.join(
                config_paths().get("data_path"),
                user_tag
            )
        )
        
# set time stamp
settings = '[out:json][timeout:180][date:"{year}-12-31T00:00:00Z"]'

# define years for download
years = [2014, 2018, 2022]
        
#--------------------------------------------------
# download data

for user_tag in user_tags:
    for year in years:
        # set extraction year
        osmnx.settings.overpass_settings = settings.format(year = year)
        
        # time out setting
        osmnx.settings.timeout = 300

        # extract data for tags and city
        tagged_data = osmnx.geometries_from_place("Germany", tags = {"amenity": user_tag})

        # add tag
        tagged_data["used_tag"] = user_tag

        # export data
        filename = (
            str(user_tag)
            + "_extracted_data",
            year,
            ".csv"
        )
        tagged_data.to_csv(
            os.path.join(
                config_paths().get("data_path"),
                user_tag,
                filename
            )
        )
        
        # add information to know where the code is at
        print(f"Extraction of {year} and {user_tag} completed!")