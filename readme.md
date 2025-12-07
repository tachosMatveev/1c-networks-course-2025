для локального запуска одного сервиса `python3 -m flask --app server.py run`

для запуска redis (на macOS) `brew services start redis`

для запуска нескольких сервисов `./start_servers_script.sh`

добавляем в конфигурацию nginx.conf: `include {путь до папки}/sites-enabled/*;`

обновляем nginx (на macOS) `brew services restart nginx`

проверяем https://localhost/notes
