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
}


def clean_text_with_attr(html_content):

    # Regular expression to match any HTML tag (consider refining based on specific needs)
    pattern = r"<[^>]*>"

    # Remove tags using re.sub while preserving whitespaces within elements
    clean_text_with_tags = re.sub(pattern, " ", html_content)

    # Remove leading/trailing whitespace and apply additional cleaning as needed
    clean_text = clean_text_with_tags.strip()

    return clean_text


st.set_page_config(
    page_title="RezBot",
)


async def main():
    browser = await pyppeteer.launcher.connect(
        browserWSEndpoint="wss://chrome.browserless.io?token=4795f0e6-6128-4155-a56f-2b09cbf14afe"
    )

    page = await browser.newPage()

    # Set custom user agent
    await page.setUserAgent(customUA)

    await page.goto(
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=hr&location=Eastern,%20Saudi%20Arabia&start=0"
    )

    jobs_url = await page.querySelectorAll('li > div:first-of-type > a[href*="jobs"]')
    for job_url in jobs_url:
        job = await job_url.getProperty("href")
        jURL = await job.jsonValue()
        with requests.Session() as s:
            r = s.get(jURL, headers=headers)
            soup = BeautifulSoup(r.content, features="lxml")
            text = [
                element.get_text(strip=True)
                for element in soup.select(".show-more-less-html__markup")
            ]
    await browser.close()
    return text


st.title("Rezbot")

# Initialize the session state for storing div elements if not already initialized
if "div_elements" not in st.session_state:
    st.session_state.div_elements = []


# Function to add new div element to the list
def add_div_element(new_element):
    st.session_state.div_elements.append(new_element)


# Text input for user to enter new div content
user_input = st.text_input("Enter new div content:", "", key="clear")

# Button to add the new div. When clicked, it calls the add_div_element function with the user_input
if st.button("Add Div"):
    if user_input:  # Check if the input is not empty
        response = asyncio.get_event_loop().run_until_complete(main())
        # print(response)
        add_div_element(response)
        st.text_input("Enter new div content:", "")  # Reset input field

# Placeholder for the fixed container
placeholder = st.empty()

# Generate the HTML for the div elements
html_content = "".join(
    f'<div class="hi">{element}</div>' for element in st.session_state.div_elements
)

# Display the HTML content within the main div, using the placeholder
placeholder.markdown(
    f'<div id="main" style="border: 2px solid #4CAF50; padding: 10px;">{html_content}</div>',
    unsafe_allow_html=True,
)
