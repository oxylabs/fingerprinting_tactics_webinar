# run: `playwright install`

import asyncio

from base import do_check

from fingerprinting_tactics_webinar.const.urls import (
    HEADLESS_TEST1,
    HEADLESS_TEST2,
    HEADLESS_TEST3,
    FINGERPRINT_STUNDZIALT,
    WEBRTC,
)

TARGET = HEADLESS_TEST1


if __name__ == '__main__':
    asyncio.run(do_check(TARGET, "check_headful", headless=False))
    asyncio.run(do_check(TARGET, "check_headless", headless=True))
    asyncio.run(do_check(TARGET, "check_headless_with_mocks", headless=True, use_mocks=True))
