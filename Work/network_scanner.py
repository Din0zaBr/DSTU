#!/usr/bin/env python
# terminal command example: python network_scanner.py -t/--target [IP 10.0.2.1/24]
"""
Этот скрипт позволяет сканировать сеть на наличие активных устройств, используя ARP-запросы.
Он принимает один аргумент командной строки -t или --target, который определяет целевой IP-адрес или диапазон IP-адресов
для сканирования. Скрипт выводит список найденных устройств с их IP-адресами и MAC-адресами.
"""
import scapy.all as scapy
import argparse


# Функция для получения аргументов командной строки
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range.")
    options = parser.parse_args()
    return options


# Функция для сканирования сети
def scan(ip):
    # Создание ARP-запроса для определенного IP-адреса
    arp_request = scapy.ARP(pdst=ip)
    # Указываем широковещательный адрес в заголовке Ethernet-пакета
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # Объединяем ARP-запрос и широковещательный пакет
    arp_request_broadcast = broadcast / arp_request
    # Отправляем ARP-запрос и получаем ответы от устройств в сети
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    # Создаем список клиентов с их IP-адресами и MAC-адресами
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


# Функция для вывода результатов сканирования
def print_result(results_lists):
    print("IP\t\t\tMAC Address\n-------------------------------------------")
    for client in results_lists:
        print(client["ip"] + "\t\t" + client["mac"])


# Получение аргументов командной строки
options = get_arguments()

# Сканирование сети и получение результатов
scan_result = scan(options.target)

# Вывод результатов сканирования
print_result(scan_result)
