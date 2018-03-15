import os
import datetime
import time


# Other functions
# ########################################################################
def last_modified():
    pass


def get_current_timestamp():
    return time.time()


def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
