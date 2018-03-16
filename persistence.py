import csv
import os

import util
import base64

# ----- Constants -----
ANSW_FILE_PATH = os.getenv('ANSW_FILE_PATH') if 'ANSW_FILE_PATH' in os.environ else "sample_data/answer.csv"
QSTN_FILE_PATH = os.getenv('QSTN_FILE_PATH') if 'QSTN_FILE_PATH' in os.environ else "sample_data/question.csv"


# ----- Transcoding function -----
def code_string(dictionary, header, key):
    """
    Transcoding dictionary value to or from base64.

    Args:
        dictionary: dictionary
        header: Dictionary header
        key: Type of cryptography

    Returns:
        Decoded/encoded string
    """
    if header in ["title", "message", "image"]:
        if key == "encode":
            return str(base64.b64encode(bytes(dictionary[header], "utf-8")))[2:-1]
        elif key == "decode":
            return base64.b64decode(bytes(dictionary[header], "utf-8")).decode("utf-8")
        else:
            raise ValueError("Wrong key!")
    else:
        return dictionary[header]


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
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for header in row:
                row[header] = code_string(row, header, "decode")
                if header in ["id", "vote_number", "view_number", "question_id"]:
                    row[header] = int(row[header])
                if header == "submission_time":
                    row[header] = float(row[header])
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
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for dictionary in data:
            for key in dictionary:
                dictionary[key] = code_string(dictionary, key, "encode")
            writer.writerow(dictionary)
