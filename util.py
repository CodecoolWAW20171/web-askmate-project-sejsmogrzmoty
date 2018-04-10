from datetime import datetime


# Other functions
# ########################################################################
def get_current_time():
    return datetime.now().replace(microsecond=0)


def convert_time_to_string(data, col_key):
    for i, _ in enumerate(data):
        data[i][col_key] = str(data[i][col_key])
    return data


def switch_null_to_default(data, defaults, ignored=()):
    for row in data:
        for key, value in row.items():
            if (value is None) and (key not in ignored):
                row[key] = defaults[key]
    return data


def hide_long_string(data, col_key):
    for i, _ in enumerate(data):
        text = data[i][col_key]
        if text.count('\n') > 4:
            data[i][col_key] = data[i][col_key][:find_nth(text, '\n', 4)+1]
        else:
            data[i][col_key] = data[i][col_key][:250]
    return data


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start
