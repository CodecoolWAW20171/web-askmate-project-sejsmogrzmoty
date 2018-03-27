import os
import datetime
import time
from datetime import datetime

# Other functions
# ########################################################################
def generate_new_id(data):
    new_id = 0
    for entry in data:
        new_id = entry['id']
    return new_id + 1


def get_current_timestamp():
    return time.time()


def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def prepare_new_entry(data, new_data, defaults):
    entry = {}
    entry['id'] = generate_new_id(data)
    entry['submission_time'] = get_current_timestamp()
    for header in defaults:
        if header in new_data:
            entry[header] = new_data[header]
        else:
            entry[header] = defaults[header]
    return entry

dt = datetime.now().replace(microsecond=0)