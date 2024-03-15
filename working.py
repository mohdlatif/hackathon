import streamlit as st
import asyncio
import pyppeteer
import nest_asyncio
import requests
from bs4 import BeautifulSoup
import json
import re

nest_asyncio.apply()


async def take_screenshot(url):
    browser = await pyppeteer.launcher.connect(
        browserWSEndpoint="wss://chrome.browserless.io?token=4795f0e6-6128-4155-a56f-2b09cbf14afe"
    )
    page = await browser.newPage()
    await page.goto(url)
    screenshot = await page.screenshot({"path": "example.png"})
    await browser.close()
    return screenshot


def run_pyppeteer_task(url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(take_screenshot(url))
    loop.close()
    return result


def main():
    st.title("Async Screenshot with Streamlit and Pyppeteer")

    url = st.text_input(
        "Enter the URL to capture:",
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=hr&location=Eastern,%20Saudi%20Arabia&start=0",
    )
    if st.button("Take Screenshot"):
        with st.spinner("Taking screenshot..."):
            run_pyppeteer_task(url)
            st.success("Screenshot taken successfully!")
            st.image("example.png")


if __name__ == "__main__":
    main()
