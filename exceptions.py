class SendMessageError(Exception):
    """Ошибка при отправке сообщения в телеграмм."""
    pass


class ApiStatusError(Exception):
    """Ошибка статуса API."""
    pass


class RequestError(Exception):
    """Ошибка при запросе к API."""
    pass
