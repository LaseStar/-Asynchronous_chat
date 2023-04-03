import copy
import unittest
from server import get_message, client_response_check, create_client_presence
from test_client import TestSocket


class TestClass(unittest.TestCase):
    test_dict_accept = {
        "action": "authenticate",
        "time": 1111.111111,
        "user": {
            "account_name": "User1",
            "password": "Password123"
        }
    }

    test_dict_accept_400_1 = copy.deepcopy(test_dict_accept)
    test_dict_accept_400_1.pop("action", None)

    test_dict_accept_400_2 = copy.deepcopy(test_dict_accept)
    test_dict_accept_400_2.pop("time", None)

    test_dict_accept_400_3 = copy.deepcopy(test_dict_accept)
    test_dict_accept_400_3.pop("user", None)

    test_dict_accept_400_4 = copy.deepcopy(test_dict_accept)
    test_dict_accept_400_4["user"].pop("account_name", None)

    test_dict_accept_400_5 = copy.deepcopy(test_dict_accept)
    test_dict_accept_400_5["user"].pop("password", None)

    test_dict_accept_401 = copy.deepcopy(test_dict_accept)
    test_dict_accept_401["action"] = "repeat"

    test_dict_accept_402_account = copy.deepcopy(test_dict_accept)
    test_dict_accept_402_account["user"]["account_name"] = "User"

    test_dict_accept_402_password = copy.deepcopy(test_dict_accept)
    test_dict_accept_402_password["user"]["password"] = "Password"

    test_dict_recv_200 = {
        'response': 200,
        'alert': 'OK'
    }
    test_dict_recv_400 = {
        'response': 400,
        'alert': 'Bad Request'
    }
    test_dict_recv_401 = {
        'response': 401,
        'alert': 'Not authorized'
    }
    test_dict_recv_402 = {
        'response': 402,
        'alert': 'wrong username/password'
    }

    def test_def_get_message(self):
        test_socket = TestSocket(self.test_dict_accept)
        self.assertEqual(get_message(test_socket), self.test_dict_accept)

    def test_def_client_response_check(self):
        self.assertEqual(client_response_check(self.test_dict_accept), self.test_dict_recv_200)
        self.assertEqual(client_response_check(self.test_dict_accept_400_1), self.test_dict_recv_400)
        self.assertEqual(client_response_check(self.test_dict_accept_400_2), self.test_dict_recv_400)
        self.assertEqual(client_response_check(self.test_dict_accept_400_3), self.test_dict_recv_400)
        self.assertEqual(client_response_check(self.test_dict_accept_400_4), self.test_dict_recv_400)
        self.assertEqual(client_response_check(self.test_dict_accept_400_5), self.test_dict_recv_400)
        self.assertEqual(client_response_check(self.test_dict_accept_401), self.test_dict_recv_401)
        self.assertEqual(client_response_check(self.test_dict_accept_402_account), self.test_dict_recv_402)
        self.assertEqual(client_response_check(self.test_dict_accept_402_password), self.test_dict_recv_402)

    def test_def_create_client_presence(self):
        test_socket = TestSocket(self.test_dict_recv_200)
        create_client_presence(self.test_dict_recv_200, test_socket)
        self.assertEqual(test_socket.received_message, test_socket.encoded_message)


if __name__ == '__main()__':
    unittest.main()
