# logmethod/utils.py

from datetime import datetime

def get_index_name(env, app_name):
    today = datetime.utcnow().strftime("%Y.%m.%d")
    return f"{env}-{app_name}-{today}"
