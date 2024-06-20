# run: `playwright install`

import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

from fingerprinting_tactics_webinar.const.proxy_auth import (
    PROXY_URL,
    PROXY_USERNAME,
    PROXY_PASSWORD,
)
from fingerprinting_tactics_webinar.const.urls import (
    TIMEZONE_INFO,
    HEADLESS_TEST1,
)

# Run `python -m playwright install` before running script.

webRTCargs = [
    "-use-fake-device-for-media-stream",  # add fake speakers, mic
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
HEADERS = {
    "User-Agent": USER_AGENT,
}
wait_until = [
        "load",
        "domcontentloaded",
        "networkidle2",
    ]


async def plugins(page, count: int = 3):
    plugins_array = ','.join(str(i) for i in range(count))
    await page.add_init_script(
        'Object.defineProperty('
        'Object.getPrototypeOf(navigator),'
        '"plugins",'
        '{get() {return [' + plugins_array + ']}})'
    )


async def mocks(
        browser,
        timezone_id: str = None,
        locale: str = None,
):
    if not timezone_id:
        page = await browser.new_page()
        await page.goto(TIMEZONE_INFO)
        content = await page.content()
        timezone_id = content.replace("<html><head></head><body>", "").replace(
            "\n</body></html>",
            "",
        )
    if not locale:
        locale = 'lt-LT'
    context = await browser.new_context(
        locale=locale,
        timezone_id=timezone_id,
        user_agent=USER_AGENT,
    )
    return context


async def get_page_with_mocks(
        browser,
        timezone_id: str = None,
        locale: str = None,
        plugins_count: int = 4,
):
    if not timezone_id:
        page = await browser.new_page()
        await page.goto(TIMEZONE_INFO)
        content = await page.content()
        timezone_id = content.replace("<html><head></head><body>", "").replace(
            "\n</body></html>",
            "",
        )
    if not locale:
        locale = 'lt-LT'
    context = await browser.new_context(
        locale=locale,
        timezone_id=timezone_id,
        user_agent=USER_AGENT,
    )
    page = await context.new_page()
    await plugins(page, plugins_count)
    return page


async def get_chromium_browser_and_page(
        playwright,
        headless: bool = True,
        use_proxy: bool = True,
        use_mocks: bool = True,
        use_stealth: bool = True,
):
    args = [
        "--start-maximized",
        "--no-sandbox",
        "--disable-setuid-sandbox",  # TODO: Chrome reports unknown flag.
        "--disable-web-security",  # CORS checks are now disabled.
        "--disable-gpu",  # Reduces CPU usage when running headful.
    ]
    args += webRTCargs
    if use_proxy:
        browser = await playwright.chromium.launch(
            headless=headless,
            args=args,
            devtools=False,
            proxy={
                'server': PROXY_URL,
                'username': PROXY_USERNAME,
                'password': PROXY_PASSWORD,
            },
        )
    else:
        browser = await playwright.chromium.launch(
            headless=headless,
            args=args,
            devtools=False,
        )

    if use_mocks:
        page = await get_page_with_mocks(browser=browser)
    else:
        page = await browser.new_page()

    if use_stealth:
        await stealth_async(page=page)

    await page.set_extra_http_headers(headers=HEADERS)

    return browser, page


async def do_check(
        target: str = HEADLESS_TEST1,
        screenshot: str = None,
        headless: bool = True,
        use_proxy: bool = False,
        use_mocks: bool = False,
        use_stealth: bool = False,
        wait: int = 3,
):
    async with async_playwright() as p:
        browser, page = await get_chromium_browser_and_page(
            p,
            headless=headless,
            use_proxy=use_proxy,
            use_mocks=use_mocks,
            use_stealth=use_stealth,
        )
        await asyncio.sleep(1)
        response = await page.goto(
            url=target,
            wait_until='networkidle',
        )
        await asyncio.sleep(wait)
        if screenshot is not None:
            await page.screenshot(path=f"{screenshot}.png", full_page=True)
        print(f"Response status to {target}: {response.status}")
