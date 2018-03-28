from datetime import datetime


# Other functions
# ########################################################################
def get_current_time():
    return datetime.now().replace(microsecond=0)
