# Activity visualiser for github users 

#todo link to habr
#todo gif image

![Summary graph](https://habrastorage.org/web/413/ebc/8cd/413ebc8cd62745ae89c51b1b38dc58c9.png)


## Концепт:

- [x] сливаем все публичные репозитории пользователя
- [x] фильтруем форки и зеркала
- [x] строим лог активности за год
- [x] запускаем по нему gource


## Usage

```
$ git clone https://github.com/esemi/github-activity-visualiser.git
$ cd github-activity-visualiser
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ sed -i -- 's/%GITHUB_TOKEN%/U_TOKEN_HERE/g' settings.py
$ ./main.py USER_NAME
```
