## geo2ban.py Мониторит access.log и по указанному фильтру добавляет IP в blackhole

установите зависимости (пакеты geoip):

`pip install -r requirements.txt`

### В скрипте сконфигурируйте следующие параметры:

- `LOGFILE = 'path/to/access.log'` (Путь до log файла)
- `WHITELIST_FILE = 'path/to/whitelist.txt'` (Путь до whitelist, требования к whitelist указаны в примере whitelist.txt)
- `BANLIST_FILE = 'path/to/banlist.txt'` (Путь до banlist файла,)
- `SLEEP_INTERVAL = 3` (Частота выборки из logfile в секундах)
- `ALLOWED_COUNTRIES = ('RU',)` (Указать список разрешенных стран через запятую https://dev.maxmind.com/geoip/legacy/codes/iso3166/)

### Тестовый и боевой режим
По умолчанию скрипт работает в тестовом режиме и не выполняет команду `ip route add blackhole {IP}`, а только вносит записи в banlist.txt.

Для запуска в боевом режиме раскомментируйте 53 строку:

`# os.system('ip route add blackhole {0}'.format(ip))`
