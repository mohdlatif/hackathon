import asyncio
import signal
import traceback
import nest_asyncio
import pyppeteer
import requests
from bs4 import BeautifulSoup
import re
import json
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

# create a strong reference to tasks since asyncio doesn't do this for you
task_references = set()


def register_ensure_future(coro):
    task = asyncio.ensure_future(coro)
    task_references.add(task)

    # Setup cleanup of strong reference on task completion...
    def _on_completion(f):
        task_references.remove(f)

    task.add_done_callback(_on_completion)

    return task


# Function to clean text
def clean_text(text):
    # Regular expression to match any HTML tag (consider refining based on specific needs)
    pattern = r"<[^>]*>"

    # Remove tags using re.sub while preserving whitespaces within elements
    clean_text_with_tags = re.sub(pattern, " ", text)

    # Remove leading/trailing whitespace and apply additional cleaning as needed
    clean_text = clean_text_with_tags.strip()

    return clean_text


def generate_html(jobs):
    html_str = '<div class="container">'
    for job in jobs:
        html_str += f"""
            <div class="ops">
                <h2>{job['Title']}</h2>
                <p>{job['Company']}</p>
                <p>{job['Location']}</p>
                <p><a href="{job['Job URL']}">Job Link</a></p>
            </div>
        """
    html_str += "</div>"
    return html_str


def generate_elemets(json_data):
    # Layout Parameters
    num_columns_per_row = 3

    # Create Columns
    columns = st.columns(num_columns_per_row)

    # Generate Divs
    for index, job in enumerate(json_data):
        column_index = index % num_columns_per_row
        with columns[column_index]:
            st.markdown(
                """
            <div class="ops">
                <h5>{}</h5>
                <p>{}</p>
                <p>{}</p>
                <a href="{}">Apply Now</a>
            </div>""".format(
                    job["Title"], job["Company"], job["Location"], job["Job URL"]
                ),
                unsafe_allow_html=True,
            )

    # Optional CSS Styling
    st.markdown(
        """
    <style>
        .ops {
            border: 1px solid lightgray;
            padding: 15px;
            margin-bottom: 20px;
            /* Add more styles as needed */
        }
         h5 {
        color: #ad7d41;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


async def fetch_jobs(url):
    browser = await pyppeteer.launcher.connect(
        browserWSEndpoint="wss://chrome.browserless.io?token=4795f0e6-6128-4155-a56f-2b09cbf14afe"
    )
    page = await browser.newPage()
    await page.setUserAgent(customUA)
    await page.goto(url)

    alljobs = []

    i_tag_count = await page.evaluate(
        """() => {
        return document.querySelectorAll('.base-card.relative').length;
    }"""
    )
    await page.screenshot({"path": "quotes.png", "fullPage": True})

    for i in range(1, i_tag_count + 1):
        job_details = {}
        job_container_selector = f"li:nth-of-type({i})"

        # (1) Fetch job title
        job_details["Title"] = clean_text(
            await page.querySelectorEval(
                f"{job_container_selector} .base-search-card__title",
                "node => node.textContent",
            )
        )

        # (2) Fetch job company
        job_details["Company"] = clean_text(
            await page.querySelectorEval(
                f"{job_container_selector} .base-search-card__subtitle",
                "node => node.textContent",
            )
        )

        # (3) Fetch job location
        job_details["Location"] = clean_text(
            await page.querySelectorEval(
                f"{job_container_selector} .job-search-card__location",
                "node => node.textContent",
            )
        )

        # Assuming the job URL is also within the i tag container
        job_href_property = await page.querySelectorEval(
            f"{job_container_selector} a[href*='jobs']", "a => a.href"
        )
        job_details["Job URL"] = job_href_property

        # Fetch job details using requests and BeautifulSoup
        # with requests.Session() as s:
        #     response = s.get(job_details["jURL"], headers=headers)
        #     soup = BeautifulSoup(response.content, features="lxml")
        #     job_details["jDetails"] = [
        #         element.get_text(strip=True)
        #         for element in soup.select(".show-more-less-html__markup")
        #     ]

        alljobs.append(job_details)

    await browser.close()
    return alljobs


# Example list of options
job_types = ["Full Time", "Part Time", "Internship", "Contract", "Remote"]


url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=hr&location=Eastern,%20Saudi%20Arabia&start=0"


async def main():
    st.title("RezBot")

    url = st.text_input(
        "Enter the URL to capture:",
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=hr&location=Eastern,%20Saudi%20Arabia&start=0",
    )
    if st.button("Fetch Jobs"):
        with st.spinner("Fetching..."):
            job_data = await fetch_jobs(url)
            st.success("Jobs Fetched!")
            if job_data:
                html_code = generate_elemets(job_data)
            else:
                st.write("No jobs found.")


if __name__ == "__main__":
    asyncio.run(main())
