# mailru-cloud (Python CLI)

Неофициальный CLI-клиент для Mail.ru Cloud, написанный на Python.

## Установка

```bash
git clone https://github.com/mueqee/mailrucloud.git
cd mailrucloud
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Команды

- `login`: Войти в облако
- `ls [REMOTE_DIR]`: Показать список файлов/папок (по умолчанию корень `/`)
- `upload <LOCAL_PATH>`: Загрузить файл в облако
- `download`: Скачать файл (пример ниже)
- `sync [OPTIONS] <LOCAL_DIR> <REMOTE_DIR>`: Синхронизация каталогов (поддерживает режимы `push`, `pull`, `both`)
- `rm <REMOTE_PATH>`: Удалить файл/папку
- `mv <SRC> <DST>`: Переименовать/переместить файл
- `info <REMOTE_PATH>`: Показать информацию о файле

### Авторизация и пароли

При первом запуске используйте команду:

`python main.py login`

CLI запросит ваш email и пароль от Mail.ru.

> ⚠️ Если у вас включена двухфакторная аутентификация (2FA), необходимо использовать пароль приложения.

#### Как получить пароль приложения

   1. Откройте: **https://account.mail.ru/user/2-step-auth/**

   2. Перейдите в раздел «Пароли приложений»

   3. Создайте новый пароль (например, MailruCloud CLI)

   4. Используйте этот пароль вместо основного при входе через login

#### Поддерживаемые почты

Поддерживаются только аккаунты Mail.ru:

   - @mail.ru
   - @inbox.ru
   - @bk.ru
   - @list.ru

    🛑 Аккаунты с доменом @vk.com не поддерживаются, даже если вы можете войти на сайт cloud.mail.ru вручную.


## Быстрый тест WebDAV

```bash
# Список содержимого
python main.py ls

# Загрузка файла
echo "hello" > ~/hello.txt
python main.py upload ~/hello.txt

# Скачивание файла
python - <<'PY'
from download import download_file
download_file('/hello.txt', '~/hello_from_cloud.txt')
PY

diff ~/hello.txt ~/hello_from_cloud.txt  # должно быть пусто
```

При выполнении `python main.py login` создаётся файл `~/.mailru_token.json`

## Синхронизация каталогов

```bash
# Двусторонняя (both — по умолчанию)
python main.py sync ~/Documents /backup

# Только загрузка локальных изменений → облако
python main.py sync ~/Documents /backup --direction push

# Только скачивание изменений из облака
python main.py sync ~/Documents /backup -d pull
```

Файлы, отсутствующие на одной из сторон, будут скопированы. Удаление пока не синхронизируется.
