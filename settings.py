import datetime

GITHUB_TOKEN = 'TODO'
TIMESTAMP_BORDER = int((datetime.datetime.utcnow() - datetime.timedelta(days=365)).timestamp())
DEBUG = False

# todo
DATA_FOLDER = 'user_logs'
REPO_TMP_FOLDER = 'tmp_repo'

try:
    from settings_local import *
except ImportError:
    pass