import logging
import sys
import log.client_log_config
import log.server_log_config

if sys.argv[0].find('client') == -1:
    # сервер
    LOGGER = logging.getLogger('server')
else:
    # клиент
    LOGGER = logging.getLogger('client')


def log(func):
    def log_func(*args, **kwargs):
        r = func(*args, **kwargs)
        LOGGER.debug(f'Функция {func.__name__} с параметрами {args}, {kwargs}. '
                     f'Вызвана из модуля {func.__module__}.')
        return r

    return log_func
