
GITHUB_TOKEN = 'TODO'
TIMESTAMP_BORDER = 1483228800
DEBUG = False

# todo
DATA_FOLDER = 'user_logs'
REPO_TMP_FOLDER = 'tmp_repo'

try:
    from settings_local import *
except ImportError:
    pass