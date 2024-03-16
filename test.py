import requests
import json
from bs4 import BeautifulSoup

customUA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

headers = {
    "user-agent": customUA,
    "Accept-Encoding": "*",
    "accept-language": "en-US,en;q=0.7",
    "Referer": "https://www.linkedin.com/",
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

# with requests.Session() as s:
#     response = s.get(
#         "https://www.linkedin.com/jobs/view/data-analyst-at-talent-disruptors-3821314457/?trackingId=vA6F1L%2Fe4YB367liBKNMsw%3D%3D&refId=HwNlIKbpGgEKbTWBPaa%2Bgw%3D%3D&pageNum=0&position=2&trk=public_jobs_jserp-result_search-card&originalSubdomain=sa",
#         headers=headers,
#     )
#     soup = BeautifulSoup(response.content, features="lxml")
#     x = [element.get_text(strip=True) for element in soup.select("#job-details")]
#     print(soup)


# ---------------------------- Clean Text ----------------------------
def clean_text(text):
    # Regular expression to match any HTML tag
    pattern = r"<[^>]*>"

    # Remove tags using re.sub while preserving whitespaces within elements
    clean_text_with_tags = re.sub(pattern, " ", text)

    # Remove leading/trailing whitespace and apply additional cleaning as needed
    clean_text = clean_text_with_tags.strip()

    return clean_text


# ---------------------------- Clean Text ----------------------------


# ---------------------------- Split Jobs by 3 columns and styling them using CSS ----------------------------


def jobs_display(jobs_display):
    # Layout Parameters
    num_columns_per_row = 3

    # Create Columns
    columns = st.columns(num_columns_per_row)

    # Assuming you have a variable `num_columns_per_row` defined
    # and a Streamlit columns setup `columns`
    for index, job in enumerate(jobs_display):
        column_index = index % num_columns_per_row
        with columns[column_index]:
            create_job_div(job, index)


def create_job_div(job, index):
    with st.container():
        st.markdown(
            f"""
            <div class="ops">
            <h2>{job['Title']}</h2>

            <p>{job['Company']}</p>
            <p>{job['Location']}</p>
            <a href="{job['Job URL']}" target="_blank">Job Details</a>
            </div>""",
            unsafe_allow_html=True,
        )
        with st.expander("See explanation"):
            st.write(job["jDetails"])


# ---------------------------- Split Jobs by 3 columns and styling them using CSS ----------------------------


# ---------------------------- Fetching Jobs and crawling their data ----------------------------
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
    # await page.screenshot({"path": "quotes.png", "fullPage": True})

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

        job_href_property = await page.querySelectorEval(
            f"{job_container_selector} a[href*='jobs']", "a => a.href"
        )
        job_details["Job URL"] = job_href_property

        # Fetch job details using requests and BeautifulSoup
        # with requests.Session() as s:
        #     response = s.get(job_details["Job URL"], headers=headers)
        #     soup = BeautifulSoup(response.content, features="lxml")
        #     job_details["jDetails"] = [
        #         element.get_text(strip=True) for element in soup.select("#job-details")
        #     ]

        await page.goto(job_details["Job URL"])
        job_details["jDetails"] = clean_text(
            await page.querySelectorEval(
                f"{job_container_selector} #job-details",
                "node => node.textContent",
            )
        )
        alljobs.append(job_details)

    await browser.close()
    return alljobs
