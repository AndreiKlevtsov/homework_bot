### Telegram-bot

```
Телеграм-бот для отслеживания статуса проверки домашней работы на Яндекс.Практикум.
Присылает сообщения, когда статус изменен - взято в проверку, есть замечания, зачтено.
Python-разработчик (бекенд) (Яндекс.Практикум)


```

### Технологии:
- Python 3.9
- python-dotenv 0.19.0
- python-telegram-bot 13.7

### Запуск проекта:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AndreiKlevtsov/homework_bot.git
```

```
cd homework_bot
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Записать в переменные окружения (файл .env) необходимые ключи:
PRACTICUM_TOKEN='токен Практикум'
TELEGRAM_TOKEN='<id бота>>'
TELEGRAM_CHAT_ID=<ваш id telegram>

ENDPOINT='эндпоинт из учебных материалов'


Запустить проект:

```
python homework.py
```