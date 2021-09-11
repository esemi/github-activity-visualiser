Github user activity visualiser 
---
- download all user's public repositories
- filter forks and mirrors
- build a one year activity log
- run a gource on it

[more details (rus)](https://habrahabr.ru/company/semrush/blog/345818/)

![КДПВ](https://habrastorage.org/webt/jq/os/wn/jqoswnphohklp8eswtsejbgtxty.gif)

### Usage
```
$ git clone https://github.com/esemi/github-activity-visualiser.git
$ cd github-activity-visualiser
$ python3.9 -m venv venv
$ source venv/bin/activate
$ pip install poetry
$ poetry config virtualenvs.create false --local
$ poetry install
$ apt install gource
### generate new token here https://github.com/settings/tokens and past on next step
$ poetry run python visualiser/visualiser.py --help
```
