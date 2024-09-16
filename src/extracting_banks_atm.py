# -------------------------------------------------
# import modules

import os
import osmnx
import pandas as pd
import shutup
from helpers.config import config_paths

#--------------------------------------------------
# set up

# Suppress specific warnings
shutup.please()

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

# define states to break up Germany into smaller parts
states = [
    "Baden-Württemberg",
    "Bayern",
    "Berlin",
    "Brandenburg",
    "Bremen",
    "Hamburg",
    "Hessen",
    "Mecklenburg-Vorpommern",
    "Niedersachsen",
    "Nordrhein-Westfalen",
    "Rheinland-Pfalz",
    "Saarland",
    "Sachsen",
    "Sachsen-Anhalt",
    "Schleswig-Holstein",
    "Thüringen"
]

#--------------------------------------------------
# color scheme for printing

class bcolors:
    REDBOLD = "\u001b[31;1m"
    GREENBOLD = "\u001b[32;1m"
    UNDERLINE = "\u001b[4m"
    ENDC = "\u001b[0m" # defines end such that only the specific line is colored

#--------------------------------------------------
# download data

for state in states:
    for user_tag in user_tags:
        for year in years:
            # set extraction year
            osmnx.settings.overpass_settings = settings.format(year = year)
            
            # time out setting
            osmnx.settings.timeout = 300

            # extract data for tags and city
            tagged_data = osmnx.geometries_from_place(state + ", Germany", tags = {"amenity": user_tag})
            
            # add tag, year, and state information
            tagged_data["used_tag"] = user_tag
            tagged_data["year"] = year
            tagged_data["state"] = state

            # export data
            filename = (
                str(user_tag)
                + "_extracted_data_"
                + str(year)
                + "_"
                + str(state)
                + ".csv"
            )

            tagged_data.to_csv(
                os.path.join(
                    config_paths().get("data_path"),
                    user_tag,
                    filename
                )
            )
            
            # add information to know where the code is at
            print(
                (f"{bcolors.GREENBOLD}Extraction for {state} of {year} and {user_tag} completed!{bcolors.ENDC}")
            )