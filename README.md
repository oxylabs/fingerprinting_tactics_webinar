Fingerprinting Tactics with Pyppeteer and Playwright Code Samples
==

<a href="https://oxylabs.io/?utm_source=github&utm_medium=referral&utm_content=fingerprinting_tactics_webinar&utm_campaign=banner&groupid=877"><img src="https://img.shields.io/badge/🚀_Get_Started-FF6B35?style=for-the-badge" alt="Get started"></a>
<a href="https://developers.oxylabs.io"><img src="https://img.shields.io/badge/📚_Documentation-4A90E2?style=for-the-badge" alt="Documentation"></a>
<a href="https://dashboard.oxylabs.io"><img src="https://img.shields.io/badge/📊_Dashboard-2EA44F?style=for-the-badge" alt="Dashboard"></a>
<a href="https://discord.gg/Pds3gBmKMH"><img src="https://img.shields.io/badge/💬_Discord-5865F2?style=for-the-badge" alt="Discord"></a>
<a href="https://www.youtube.com/@oxylabs"><img src="https://img.shields.io/badge/▶️_YouTube-FF0000?style=for-the-badge" alt="YouTube"></a>

These are the base code samples used during the "Fingerprinting Tactics with Pyppeteer and Playwright Code Samples" webinar by Oxylabs.

Tested with python3.10

Requirements:
```
pip install -r requirements.txt
```

When running pyppeteer samples, headful mode might not work unless this environment variable is set:
```
PYPPETEER_CHROMIUM_REVISION=747023
```

Proxy authentication info is contained in `proxy_auth.py` files:
```python
PROXY_URL = "http://pr.oxylabs.io:7777"
PROXY_USERNAME = "user"
PROXY_PASSWORD = "password"
```
Change these constants to your credentials.
