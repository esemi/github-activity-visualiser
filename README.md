# Activity visualiser for github users 

https://habrahabr.ru/company/semrush/blog/345818/

![КДПВ](https://habrastorage.org/webt/jq/os/wn/jqoswnphohklp8eswtsejbgtxty.gif)

## Концепт:

- [x] сливаем все публичные репозитории пользователя
- [x] фильтруем форки и зеркала
- [x] строим лог активности за год
- [x] запускаем по нему gource


## Usage

```
$ git clone https://github.com/esemi/github-activity-visualiser.git
$ cd github-activity-visualiser
$ virtualenv -p python3.6 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ sed -i -- 's/%GITHUB_TOKEN%/U_TOKEN_HERE/g' settings.py

$ ./main.py USER_NAME
```
