import asyncio
import random

import pyppeteer
from pyppeteer.page import Page, Request
from pyppeteer.browser import Browser
from pyppeteer_stealth import stealth

from fingerprinting_tactics_webinar.const.proxy_auth import (
    PROXY_URL,
    PROXY_USERNAME,
    PROXY_PASSWORD,
)
from fingerprinting_tactics_webinar.const.urls import (
    HEADLESS_TEST1,
    TIMEZONE_INFO,
)

options = {
    "waitUntil": [
        "load",
        "domcontentloaded",
        "networkidle2",
    ],
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
HEADERS = {
    "User-Agent": USER_AGENT
}


async def do_check(
        target: str = HEADLESS_TEST1,
        screenshot: str = None,
        full_screenshot: bool = True,
        headless: bool = False,
        use_proxy: bool = False,
        use_mocks: bool = False,
        use_stealth: bool = False,
        fake_audio: bool = False,
        wait: int = 3,
):
    browser, page = await get_browser_and_page(
        headless=headless,
        use_proxy=use_proxy,
        use_stealth=use_stealth,
        headers=HEADERS,
        fake_audio=fake_audio,
    )

    await asyncio.sleep(1)

    if use_mocks:
        await timezone(page)
        await history(page, 5)
        await plugins(page, 3)
        await platform(page, "Win64")
        await navigator_ua(page, USER_AGENT, platform="Win64")
    response = await page.goto(
        url=target,
        options=options,
    )
    print("Response status: ", response.status)
    print("Response headers: ", response.headers)

    await asyncio.sleep(wait)

    if screenshot is not None:
        await page.screenshot(
            options={
                "path": f"{screenshot}.png",
                "fullPage": full_screenshot,
            }
        )
    await browser.close()


async def get_browser_and_page(
        headless: bool = True,
        use_proxy: bool = False,
        fake_audio: bool = False,
        headers: dict = None,
        use_stealth: bool = False,
        request_interception: bool = False,
) -> (Browser, Page):
    args = [
        "--start-maximized",
        "--no-sandbox",
        "--disable-web-security",  # CORS checks are now disabled.
        "--disable-gpu",  # Reduces CPU usage when running headful.
    ]
    if fake_audio:
        # Add fake audio input/output devices.
        args.append("-use-fake-device-for-media-stream")
    if use_proxy:
        args.append(f"--proxy-server={PROXY_URL}")
    browser = await pyppeteer.launch(
        args=args,
        options={
            # "executablePath": "/home/stundzia/.local/share/pyppeteer/local-chromium/1181205",
            "headless": headless,
            "autoClose": False,
            "waitUntil": [
                "load",
                "domcontentloaded",
                "networkidle2",
            ],
        }
    )

    pages = await browser.pages()
    print("Browser version: ", await browser._getVersion())
    page = pages[0]

    if headers:
        await page.setExtraHTTPHeaders(headers=headers)
    if use_stealth:
        await stealth(page)
    if use_proxy:
        await page.authenticate(
            credentials={
                "username": PROXY_USERNAME,
                "password": PROXY_PASSWORD,
            },
        )
    if request_interception:
        page.on(
            'request',
            lambda req: asyncio.ensure_future(request_intercept(req)),
        )
    return browser, page


async def platform(page: Page, platform: str = ""):
    if platform != "":
        ev = (
            "navigator.__defineGetter__('platform', function(){return 'foo'})"
            .replace("foo", platform)
        )
        await page.evaluateOnNewDocument(ev)


async def navigator_ua(page: Page, ua: str, platform: str):
    override = {
        'userAgent': ua,
        'platform': platform,
        'userAgentMetadata': {
            #   'brands': '',
            #   'fullVersion': '',
            'platform': platform,
            #   'platformVersion': '',
            #   'architecture': '',
            #   'model': '',
            #   'mobile': False,
        }
    }

    await page._client.send('Network.setUserAgentOverride', override)
    # await page._client.send('Emulation.setUserAgentOverride', override)


async def timezone(page: Page, timezone_id: str = ""):
    if not timezone_id:
        await page.goto(TIMEZONE_INFO)
        content = await page.content()
        timezone_id = content.replace("<html><head></head><body>", "").replace("\n</body></html>", "")
    await page._networkManager._client.send(
        "Emulation.setTimezoneOverride", {"timezoneId": timezone_id},
    )


async def history(page: Page, length: int = -1):
    if length == -1:
        length = random.randint(5, 25)
    await page.evaluateOnNewDocument(
        """
        () => {
            if (history.length <= 2) {
        """
        +
        f"for (i = 0; i < {length}; i++)" +
        """{
                    history.pushState({page: i}, "")
                }
            }
        }
        """
    )


async def plugins(page: Page, count: int = 3):
    plugins_array = ','.join(str(i) for i in range(count))
    await page.evaluateOnNewDocument(
        'Object.defineProperty('
        'Object.getPrototypeOf(navigator),'
        '"plugins",'
        '{get() {return [' + plugins_array + ']}})'
    )


async def request_intercept(req: Request):
    req.__setattr__('_allowInterception', True)
    if req.url.startswith('http'):
        print(f"\nreq.url: {req.url}")
        print(f"  req.resourceType: {req.resourceType}")
        print(f"  req.method: {req.method}")
        print(f"  req.postData: {req.postData}")
        print(f"  req.headers: {req.headers}")
        print(f"  req.response: {req.response}")
    return await req.continue_()
