#!/usr/bin/env python
# terminal command example: python mac_changer.py -i [network interface (eth0)] -m [mac address]
"""
Этот скрипт позволяет изменять MAC-адрес сетевого интерфейса компьютера через командную строку.
Он принимает два аргумента: имя сетевого интерфейса (-i или --interface) и новый MAC-адрес (-m или --mac).
Скрипт сначала выводит текущий MAC-адрес интерфейса, затем меняет его на указанный и проверяет, был ли MAC-адрес
успешно изменен.
"""
import subprocess
import optparse
import re


# Функция для получения аргументов командной строки
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    options, arguments = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")
    return options


# Функция для изменения MAC-адреса сетевого интерфейса
def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


# Функция для получения текущего MAC-адреса сетевого интерфейса
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


# Получение аргументов командной строки
options = get_arguments()

# Получение текущего MAC-адреса
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

# Изменение MAC-адреса
change_mac(options.interface, options.new_mac)

# Проверка успешности изменения MAC-адреса
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")
