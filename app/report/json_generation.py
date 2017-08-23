import os
from flask import json
from config import Files

BASE_DIRECTORY_REPORTS = Files.REPORTS_FOLDER


def save_json_report_to_file(json_data: dict, year: int, month: int, name: str):
    """
    Save data from a json to a file in the reports folder
    :param json_data: Json data
    :param year: year of the report
    :param month: month of the report
    :param name: name of the json file
    :return: None
    """

    file_folder = BASE_DIRECTORY_REPORTS + "/" + str(year) + "/" + str(month) + "/"
    file_name = name + str(month) + "_" + str(year) + ".json"

    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    with open(file_folder + file_name, "w") as outfile:
        json.dump(json_data, outfile, indent=4, sort_keys=False)
