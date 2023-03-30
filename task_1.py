"""
Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться
доступность сетевых узлов. Аргументом функции является список, в котором каждый сетевой
узел должен быть представлен именем хоста или ip-адресом. В функции необходимо
перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с
помощью функции ip_address().
"""
from ipaddress import ip_address
from subprocess import Popen, PIPE


def host_ping(ip_list, timeout=600, requests=1):
    results = {'Узел доступен': "", 'Узел недоступен': ""}
    for ip in ip_list:
        try:
            ip = ip_address(ip)
        except ValueError:
            pass
        proc = Popen(f"ping {ip} -w {timeout} -n {requests}", shell=False, stdout=PIPE)
        proc.wait()

        if proc.returncode == 0:
            results['Узел доступен'] += f'{str(ip)}\n'
            print(f'{ip} - Узел доступен')
        else:
            results['Узел недоступен'] += f'{str(ip)}\n'
            print(f'{ip} - Узел недоступен')
    return results


if __name__ == "__main__":
    host_ping(['google.com', '2.2.2.2', '192.168.1.1'])

"""
Результаты:
google.com - Узел доступен
2.2.2.2 - Узел недоступен
192.168.1.1 - Узел доступен
"""
