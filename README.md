Fingerprinting Tactics with Pyppeteer and Playwright Code Samples
==

[![](https://dcbadge.limes.pink/api/server/Pds3gBmKMH?style=for-the-badge&theme=discord)](https://discord.gg/Pds3gBmKMH) [![YouTube](https://img.shields.io/badge/YouTube-Oxylabs-red?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@oxylabs)

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
