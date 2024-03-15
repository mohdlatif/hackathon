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
    # await page.type("#session_key", login_user)
    # await page.type("#session_password", login_pass)
    # await page.click('button[data-id="sign-in-form__submit-btn"]')
    # await page.waitFor(5000)

    jobs_url = await page.querySelectorAll('li > div:first-of-type > a[href*="jobs"]')
    for job_url in jobs_url:
        job = await job_url.getProperty("href")
        jURL = await job.jsonValue()
        # await page.goto(jURL)
        # await page.screenshot({"path": "quotes.png"})
        # element = await page.querySelector(".show-more-less-html__markup")
        # content = await page.evaluate("(element) => element.textContent", element)
        # print(content)

        with requests.Session() as s:
            r = s.get(jURL, headers=headers)
            soup = BeautifulSoup(r.content, features="lxml")
            text = [
                element.get_text(strip=True)
                for element in soup.select(".show-more-less-html__markup")
            ]
            # print(text)

            # Method 2
            # text = soup.select(".show-more-less-html__markup")
            # # Extract and clean the text from each element
            # for element in text:
            #     clean_text = clean_text_with_attr(
            #         element.get_text()
            #     )  # Extract plain text with optional cleaning
            #     print(clean_text)

        # print(jURL)
        # print("------------")
    # await page.screenshot({"path": "quotes.png"})

    ## Get HTML
    # htmlContent = await page.content()
    await browser.close()
    return text


st.title("Rezbot")
st.image("RezBot.png")

with stylable_container(
    key="title_description",
    css_styles="""
    p {
            font-style: italic;
            margin: 12px 0;

    }
    """,
):
    st.markdown(
        "RezBot is an AI assistant that helps job seekers create impressive CVs and easily apply for suitable job openings. Users can have a conversational chat with the bot to describe their skills, experience and qualifications. The bot will then automatically generate a well-formatted CV based on the user's profile. It analyzes the CV and searches for job listings on popular job sites that match the user's abilities. Eligible openings are recommended to the user, who can quickly apply with one click directly through the bot. RezBot provides a fast and easy end-to-end process for job seekers to highlight their talents and significantly increase their chances of standing out from the crowd."
    )


c1, c2 = st.columns(2)

with c1:
    with stylable_container(
        key="text_description",
        css_styles="""
        p {
            font-size: 25px;
            color: lightblue;
            font-weight:800;
        }
        """,
    ):
        st.markdown("This is a text ")

with c2:
    st.markdown("This is the right column")

c3, c4 = st.columns(2)
with c3:

    first_name = st.text_input("First name", "", placeholder="Ahmed")
    # st.write("The current movie title is", first_name)
with c4:

    last_name = st.text_input("Last name", "", placeholder="Abdulatef")
    # st.write("The current movie title is", last_name)


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
