Github user activity visualiser 
---
[![release](https://github.com/esemi/github-activity-visualiser/actions/workflows/release.yml/badge.svg)](https://github.com/esemi/github-activity-visualiser/actions/workflows/release.yml)
[![PyPI version](https://badge.fury.io/py/github-activity-visualiser.svg)](https://pypi.org/project/github-activity-visualiser/)

- download all user's public repositories
- filter forks and mirrors
- build a one year activity log
- run a gource on it

### Usage
U need [token](https://github.com/settings/tokens) before use.
```
$ pip install github-activity-visualiser
$ visualiser --help
```

![КДПВ](https://habrastorage.org/webt/jq/os/wn/jqoswnphohklp8eswtsejbgtxty.gif)

[more details (rus)](https://habrahabr.ru/company/semrush/blog/345818/)

### Run from source
```
$ git clone https://github.com/esemi/github-activity-visualiser.git
$ cd github-activity-visualiser
$ python3.9 -m venv venv
$ source venv/bin/activate
$ pip install poetry
$ poetry config virtualenvs.create false --local
$ poetry install
$ apt install gource
$ poetry run python github_activity_visualiser/visualiser.py --help
```
