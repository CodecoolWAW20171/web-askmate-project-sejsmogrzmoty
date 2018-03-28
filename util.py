from datetime import datetime


# Other functions
# ########################################################################
def get_current_time():
    return datetime.now().replace(microsecond=0)


def convert_time_to_string(data, col_key):
    for i, _ in enumerate(data):
        data[i][col_key] = str(data[i][col_key])
    return data
