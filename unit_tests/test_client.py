"""Unit-тесты утилит"""
import json
import unittest
from client import create_presence, send_message, get_message, parse_message


class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode('utf-8')
        self.received_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode('utf-8')


class TestClass(unittest.TestCase):
    test_dict_send = {
        "action": "authenticate",
        "time": 1111.111111,
        "user": {
            "account_name": "User1",
            "password": "Password123"
        }
    }

    test_dict_recv_200 = {
        'response': 200,
        'alert': 'OK'
    }
    test_dict_recv_400 = {
            'response': 401,
            'alert': 'Not authorized'
    }
    test_dict_recv_401 = {
            'response': 402,
            'alert': 'wrong username/password'
    }

    def test_def_create_presence(self):
        test = create_presence()
        test["time"] = 1111.111111
        self.assertEqual(test, self.test_dict_send)

    def test_def_send_message(self):
        test_socket = TestSocket(self.test_dict_send)
        send_message(self.test_dict_send, test_socket)
        self.assertEqual(test_socket.received_message, test_socket.encoded_message)

    def test_def_get_message(self):
        test_socket_200 = TestSocket(self.test_dict_recv_200)
        test_socket_400 = TestSocket(self.test_dict_recv_400)
        test_socket_401 = TestSocket(self.test_dict_recv_401)

        self.assertEqual(get_message(test_socket_200), self.test_dict_recv_200)
        self.assertEqual(get_message(test_socket_400), self.test_dict_recv_400)
        self.assertEqual(get_message(test_socket_401), self.test_dict_recv_401)

    def test_def_parse_message(self):
        self.assertRaises(ValueError, parse_message, {'alert': 'Bad Request'})
        self.assertRaises(ValueError, parse_message, {'alert': 'Not authorized'})
        self.assertRaises(ValueError, parse_message, {'alert': 'wrong username/password'})


if __name__ == '__main__':
    unittest.main()
