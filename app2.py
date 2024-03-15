import asyncio
import pyppeteer
import nest_asyncio
import requests
from bs4 import BeautifulSoup
import streamlit as st


from streamlit_float import *
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.vertical_slider import vertical_slider
from streamlit_modal import Modal
import streamlit.components.v1 as components


nest_asyncio.apply()

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


async def fetch_jobs(url):
    browser = await pyppeteer.launcher.connect(
        browserWSEndpoint="wss://chrome.browserless.io?token=4795f0e6-6128-4155-a56f-2b09cbf14afe"
    )
    page = await browser.newPage()
    await page.setUserAgent(customUA)
    await page.goto(url)

    jobs_url = await page.querySelectorAll('li > div:first-of-type > a[href*="jobs"]')
    all_text = []
    for job_url in jobs_url:

        job = await job_url.getProperty("href")
        jtitle = await page.querySelectorAll('li > div:first-of-type > a[href*="jobs"]')
        jcompany = await page.querySelectorAll("li .base-search-card__subtitle")
        jlocation = await page.querySelectorAll("li .job-search-card__location")

        jURL = await job.jsonValue()

        with requests.Session() as s:
            r = s.get(jURL, headers=headers)
            soup = BeautifulSoup(r.content, features="lxml")
            jDetails = [
                element.get_text(strip=True)
                for element in soup.select(".show-more-less-html__markup")
            ]
            all_text.extend(jDetails)

    await browser.close()
    return all_text


def run_pyppeteer_task(url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(fetch_jobs(url))
    loop.close()
    return result


# Example list of options
job_types = ["Full Time", "Part Time", "Internship", "Contract", "Remote"]


def main():
    st.title("RezBot")

    url = st.text_input(
        "Enter the URL to capture:",
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=hr&location=Eastern,%20Saudi%20Arabia&start=0",
    )
    if st.button("Fetch Jobs"):
        with st.spinner("Fetching..."):
            x = run_pyppeteer_task(url)
            st.success("Jobs Fetched!")
            if x:
                for item in x:
                    st.markdown(item)
            else:
                st.write("No jobs found.")

    job_type_selected = st.selectbox(
        "Select Job Type",
        options=job_types,  # Use the list to dynamically generate options
        index=0,  # Default selection (optional)
    )

    # Float feature initialization
    float_init()

    # Initialize session variable that will open/close dialog
    if "show" not in st.session_state:
        st.session_state.show = False

    # Button that opens the dialog
    if st.button("Contact us"):
        st.session_state.show = True
        st.rerun()

    # Create Float Dialog container
    dialog_container = float_dialog(st.session_state.show)

    # Add contents of Dialog including button to close it
    with dialog_container:
        st.header("Contact us")
        name_input = st.text_input("Enter your name", key="name")
        email_input = st.text_input("Enter your email", key="email")
        message = st.text_area("Enter your message", key="message")
        if st.button("Send", key="send"):
            # ...Handle input data here...
            st.session_state.show = False
            st.rerun()


modal = Modal(
    "Demo Modal",
    key="demo-modal",
    # Optional
    padding=20,  # default value
    max_width=744,  # default value
)
open_modal = st.button("Open")
if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        st.write("Text goes here")

        html_string = """
        <h1>HTML string in RED</h1>

        <script language="javascript">
          document.querySelector("h1").style.color = "red";
        </script>
        """
        components.html(html_string)

        st.write("Some fancy text")
        value = st.checkbox("Check me")
        st.write(f"Checkbox checked: {value}")


if __name__ == "__main__":
    main()
