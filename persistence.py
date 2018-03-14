import csv
import os

import util


# ----- Constants -----
QSTN_FILE_PATH = ''
ANSW_FILE_PATH = ''


# Get functions
# ########################################################################
'''
Processes data from a csv file to a list of dictionaries.
1 row = 1 dictionary
Keys are taken from the first row

Args:
        a name of a csv file
Returns:
        a list of dictionaries

'''
def get_data_from_file(filename):
    with open(filename) as f:
        data = [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]
    return data



# Write functions
# ########################################################################
def write_data_to_file(data, filename):
    pass
