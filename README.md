Github user activity visualiser 
---
[description (rus)](https://habrahabr.ru/company/semrush/blog/345818/)

![КДПВ](https://habrastorage.org/webt/jq/os/wn/jqoswnphohklp8eswtsejbgtxty.gif)

- download all user's public repositories
- filter forks and mirrors
- build a one year activity log
- run a gource on it


### Usage

```
$ git clone https://github.com/esemi/github-activity-visualiser.git
$ cd github-activity-visualiser
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ sed -i -- 's/%GITHUB_TOKEN%/U_TOKEN_HERE/g' settings.py

$ ./main.py USER_NAME
```
