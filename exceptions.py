class SendMessageError(Exception):
    """Ошибка при отправке сообщения в телеграмм"""

    def __init__(self, *args, **kwargs):
        pass


class ApiStatusError(Exception):
    """Ошибка при запросе к API"""

    def __init__(self, *args, **kwargs):
        pass


class SendMessageException(Exception):
    """Ошибка при отправке сообщения в телеграмм"""

    def __init__(self, *args, **kwargs):
        pass
