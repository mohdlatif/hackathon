import asyncio
import pyppeteer
import requests
from bs4 import BeautifulSoup
import json
import re
import streamlit as st
from streamlit_extras.stylable_container import stylable_container

login_user = "linkedin@email.sendithere.co"
login_pass = "z2!mVNLSdT@SP#%EGT68bU8Y!GuJjT5NB7!$9ZU3RaVwp"


# Custom user agent
customUA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"


headers = {
    "user-agent": customUA,
    "Accept-Encoding": "*",
    "accept-language": "en-US,en;q=0.7",
    "Referer": "https://jadarat.sa/Jadarat/ExploreJobs?JobTab=1",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "Sec-Ch-Ua-Mobile": '"?0"',
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "origin": "https://jadarat.sa",
    "Outsystems-Locale": "ar-SA",
    "upgrade-insecure-requests": "1",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
}


async def main():
    browser = await pyppeteer.launcher.connect(
        browserWSEndpoint="wss://chrome.browserless.io?token=4795f0e6-6128-4155-a56f-2b09cbf14afe"
    )

    page = await browser.newPage()

    # Set custom user agent
    await page.setUserAgent(customUA)

    await page.goto("https://jadarat.sa/Jadarat/ExploreJobs?JobTab=1")
    # await page.type("#session_key", login_user)
    # await page.type("#session_password", login_pass)
    # await page.click('button[data-id="sign-in-form__submit-btn"]')
    await page.waitFor(5000)
    await page.screenshot({"path": "quotes.png"})
    jobs_url = await page.querySelectorAll(".heading4.OSFillParent")
    for job_url in jobs_url:
        job = await page.evaluate("(element) => element.textContent", element)
        print(job)

    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
