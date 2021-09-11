Github user activity visualiser 
---
- download all user's public repositories
- filter forks and mirrors
- build a one year activity log
- run a gource on it

[more details (rus)](https://habrahabr.ru/company/semrush/blog/345818/)

![КДПВ](https://habrastorage.org/webt/jq/os/wn/jqoswnphohklp8eswtsejbgtxty.gif)

### Usage

U need [token](https://github.com/settings/tokens) for this tool
todo

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
