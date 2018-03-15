import csv
import os

import util
import base64

# ----- Constants -----
ANSW_FILE_PATH = os.getenv('ANSW_FILE_PATH') if 'ANSW_FILE_PATH' in os.environ else "sample_data/answer.csv"
QSTN_FILE_PATH = os.getenv('QSTN_FILE_PATH') if 'QSTN_FILE_PATH' in os.environ else "sample_data/question.csv"


# Get functions
# ########################################################################
def get_data_from_file(filename):
    """
    Reads csv file and returns it as a list of dictionaries.
    Lines are rows columns are separated by ","

    Args:
        file_name (str): name of file to read

    Returns:
        List of dictionaries read from a file.
    """
    result = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for header in row:
                print(header)
                row[header] = code_string(row, header, "decode")
            result.append(row)
    return result


# Write functions
# ########################################################################
def write_data_to_file(data, filename, header):
    """
    Writes list of dictionaries into a csv file with base64 encoding.

    Args:
        file_name (str): name of file to write to
        data: list of dictionaries to write to a file
        header: Dictionary header

    Returns:
        None
    """
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for dictionary in data:
            for key in dictionary:
                dictionary[key] = code_string(dictionary, key, "encode")
            writer.writerow(dictionary)
