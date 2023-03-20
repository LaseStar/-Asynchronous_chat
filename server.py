"""Программа-сервер
● принимает сообщение клиента;
● формирует ответ клиенту;
● отправляет ответ клиенту;
● имеет параметры командной строки:
    ○ -p <port> — TCP-порт для работы (по умолчанию использует 7777);
    ○ -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все
    доступные адреса).
"""
import logging
import log.server_log_config
from socket import *
import json
import sys
from decorators import log

# Параметры логирования
SERVER_LOGGER = logging.getLogger('server')


@log
def get_message(client):
    client_gm = client.recv(1000)
    if isinstance(client_gm, bytes):
        js_resp = client_gm.decode('utf-8')
        resp = json.loads(js_resp)
        if isinstance(resp, dict):
            return resp
        raise ValueError
    raise ValueError


@log
def client_response_check(msg_crch):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {msg_crch}')
    if 'action' not in msg_crch \
            or 'time' not in msg_crch \
            or 'user' not in msg_crch \
            or 'account_name' not in msg_crch['user'] \
            or 'password' not in msg_crch['user']:
        return {
            'response': 400,
            'alert': 'Bad Request'
        }

    if msg_crch['action'] != 'authenticate':
        return {
            'response': 401,
            'alert': 'Not authorized'
        }

    if msg_crch['user']['account_name'] != 'User1' \
            or msg_crch['user']['password'] != 'Password123':
        return {
            'response': 402,
            'alert': 'wrong username/password'
        }

    return {
        'response': 200,
        'alert': 'OK'
    }


@log
def create_client_presence(msg_ccp, client_ccp):
    js_msg = json.dumps(msg_ccp)
    encod_js_msg = js_msg.encode('utf-8')
    client_ccp.send(encod_js_msg)


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = 7777
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.critical(f'Попытка запуска сервера без указания порта.')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта {listen_port}.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        SERVER_LOGGER.critical(f'Попытка запуска сервера без указания адреса, который будет слушать сервер.')
        sys.exit(1)

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((listen_address, listen_port))
    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. ')
    s.listen(5)

    while True:
        client, addr = s.accept()
        SERVER_LOGGER.info(f'Установлено соедение с ПК {addr}')
        try:
            msg_from_client = get_message(client)
            SERVER_LOGGER.debug(f'Получено сообщение {msg_from_client}')
            response = client_response_check(msg_from_client)
            SERVER_LOGGER.info(f'Cформирован ответ клиенту {response}')
            create_client_presence(response, client)
            SERVER_LOGGER.debug(f'Соединение с клиентом {addr} закрыто.')
            client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать JSON строку, полученную от '
                                f'клиента {addr}. Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()
