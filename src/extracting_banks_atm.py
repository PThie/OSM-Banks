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
        
#--------------------------------------------------
# download data

for user_tag in user_tags:
    # time out setting
    osmnx.settings.timeout = 300

    # extract data for tags and city
    tagged_data = osmnx.geometries_from_place("Germany", tags = {"amenity": user_tag})

    # add tag
    tagged_data["used_tag"] = user_tag

    # export data
    filename = (
        str(user_tag)
        + "_extracted_data.csv"
    )
    tagged_data.to_csv(
        os.path.join(
            config_paths().get("data_path"),
            user_tag,
            filename
        )
    )