import telegram
import logging
import os
import sys
import time
from http import HTTPStatus

import requests

from requests import Response

from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверяет доступность переменных окружения."""
    return all([TELEGRAM_TOKEN, PRACTICUM_TOKEN, TELEGRAM_CHAT_ID])


def send_message(bot, message):
    """Отправляет сообщение об изменении статуса."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug(message)
    except Exception as error:
        logging.error(error)


def get_api_answer(timestamp) -> dict:
    """Отправляет запрос к API Практикум.Домашка."""
    try:
        homework_statuses: Response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp}
        )
        if homework_statuses.status_code != HTTPStatus.OK:
            logging.error(
                f'Эндпоинт недоступен, ошибка: {homework_statuses.status_code}'
            )
            raise Exception(
                f'Эндпоинт недоступен, ошибка: {homework_statuses.status_code}')
        return homework_statuses.json()
    except Exception as error:
        logging.error(
            f'Эндпоинт недоступен, ошибка: {error}'
        )
        raise SystemError(
            f'Эндпоинт недоступен, ошибка: {error}'
        )


def check_response(response: dict) -> list:
    """Проверяет ответ API на соответствие документации."""
    if not response:
        message = 'Ответ от API пуст.'
        logging.error(message)
        raise Exception(message)
    if 'homeworks' not in response:
        raise TypeError(
            'Неверный формат ответа: отсутствует ключ "homeworks"')
    if not isinstance(response, dict):
        logging.error(
            f'Структура данных не соответсвует ожиданиям'
        )
        raise TypeError()
    if not isinstance(response['homeworks'], list):
        logging.error(
            f'Структура данных не соответсвует ожиданиям'
        )
        raise TypeError()
    return response['homeworks']


def parse_status(homework):
    """Проверка статуса домашней работы."""
    if 'homework_name' not in homework:
        raise KeyError('В ответе отсутсвует ключ homework_name')
    homework_name = homework.get('homework_name')
    verdict = homework.get('status')
    if verdict not in HOMEWORK_VERDICTS:
        raise ValueError(f'Неизвестный статус работы - {verdict}')
    return (f'Изменился статус проверки работы "{homework_name}".'
            f'{HOMEWORK_VERDICTS[verdict]}')


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logging.critical('Отсутствует необходимая переменная окружения!')
        sys.exit('Отсутсвуют переменные окружения')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    current_review = {
        'hw_name': '',
        'hw_status': '',
    }
    previous_review = current_review.copy()
    while True:
        try:
            response = get_api_answer(timestamp)
            new_homework = check_response(response)
            if new_homework:
                homework = new_homework[0]
                current_review[
                    'hw_name', 'hw_status'
                ] = homework.get(
                    'homework_name', 'status'
                )
                message = parse_status(homework)
                send_message(bot, message)
            else:
                current_review['hw_status'] = 'Нет обновлений статуса.'
            if current_review != previous_review:
                message = f'Текущий статус : {current_review["hw_status"]}'
                send_message(bot, message)
                previous_review = current_review.copy()
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename='log.txt',
        filemode='w',
        format='%(asctime)s, %(levelname)s,'
               ' %(message)s, %(name)s, %(funcName)s,'
               ' %(lineno)d, %(message)s'
    ),
    handlers = logging.StreamHandler(sys.stdout)
    main()
