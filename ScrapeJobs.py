import requests
from bs4 import BeautifulSoup
import json
import pyppeteer
from threading import Thread
import asyncio

# This part of the code, will use puptteer to check jobs in saudi arabia location in Linkedin and Indeed
Linkedin = "https://www.linkedin.com/authwall?trk=qf&original_referer=https://www.linkedin.com/jobs/search?trk=organization_guest_guest_nav_menu_jobs&position=1&pageNum=0&sessionRedirect=https%3A%2F%2Fwww.linkedin.com%2Fjobs%2Fsearch%3Fkeywords%3D%26location%3DSaudi%2BArabia%26geoId%3D100459316%26trk%3Dpublic_jobs_jobs-search-bar_search-submit#main-content"


async def xyr():
    browser = await pyppeteer.launcher.connect(
        browserWSEndpoint="wss://chrome.browserless.io?token=4795f0e6-6128-4155-a56f-2b09cbf14afe"
    )
    page = await browser.newPage()
    url = Linkedin
    await page.goto(url)

    input_elements = await page.querySelectorAll('input[name="loginCsrfParam"]')
    name_values = []
    # Iterate over the input elements and retrieve their name and value attributes
    for input_element in input_elements:
        name = await input_element.getProperty("name")
        value = await input_element.getProperty("value")
        name_value = {"name": await name.jsonValue(), "value": await value.jsonValue()}
        name_values.append(name_value)
    print(name_values)

    await browser.close()
    return name_values


def run_xyr():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(xyr())
    loop.close()
    # Scrape(result)
    # return result


def start():

    thread = Thread(target=run_xyr)
    thread.start()
    result = thread.join()


run_xyr()


def Scrape():
    headers_ = headers.headers
    global number_of_zip_files, status, xy

    payload = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Encoding": "*",
        "accept-language": "en-US,en;q=0.7",
        "Referer": "https://www.google.com/",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "username": "brind.x@protonmail.com",
        "password": "GzEVJXJVGLMX",
        "rememberme": "forever",
        "_wp_http_referer": "/my-account/",
        "login": "Log in",
    }

    url = "https://mybrindle.com/my-account/"

    headers_["origin"] = "https://mybrindle.com"
    headers_["Referer"] = url

    with requests.Session() as s:
        r = s.get(url, headers=headers_)
        soup = BeautifulSoup(r.content, features="lxml")
        payload["woocommerce-login-nonce"] = soup.find(
            "input", attrs={"name": "woocommerce-login-nonce"}
        )["value"]

        r = s.post(url, data=payload, headers=headers_)

        # Visiting Download Page
        r = s.get("https://mybrindle.com/my-account/api-downloads/", headers=headers_)
        soup = BeautifulSoup(r.content, features="lxml")

        # Select the elements using the CSS selectors
        FileURLs = soup.select('a[href*="am_download_file"]')

        # Set name here if one file will be downloaded.
        Filename = (
            "Brindle Booking "
            + soup.select('td[class="api-manager-version"]')[0].text.strip()
            + ".zip"
        )

        GoogleDriveID = "18OPX8gXpt2hhF4nDuzRVNh6HeegUFZx2"

        HandleBeforeDownload.checkFiles(FileURLs, Filename, GoogleDriveID, headers_, s)

        xy = HandleBeforeDownload.xy
        status = HandleBeforeDownload.status
        number_of_zip_files = HandleBeforeDownload.number_of_zip_files
