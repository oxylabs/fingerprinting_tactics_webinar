import asyncio

from base import do_check

from fingerprinting_tactics_webinar.const.urls import (
    HEADLESS_TEST1,
    HEADLESS_TEST2,
    HEADLESS_TEST3,
)


if __name__ == '__main__':
    asyncio.run(do_check(HEADLESS_TEST1, "easy_headless1", headless=True, use_stealth=True))
    asyncio.run(do_check(HEADLESS_TEST2, "easy_headless2", headless=True, use_stealth=True))
    asyncio.run(do_check(HEADLESS_TEST3, "easy_headless3", headless=True, use_stealth=True))
