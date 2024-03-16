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
from streamlit_modal import Modal

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# from streamlit_chat import message

# Load the environment variables from .env file
load_dotenv()


nest_asyncio.apply()
# create a strong reference to tasks since asyncio doesn't do this
task_references = set()

# ---------------------------- HTTP Headers for pyppeteer, requests  to fetch jobs ----------------------------
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
# ---------------------------- HTTP Headers for pyppeteer, requests  to fetch jobs ----------------------------


# ---------------------------- Setting the API keys ----------------------------

# I suppose to hide my APIs, but for transparency I decided to share them.
openai_api_key = os.getenv("OPENAI_API_KEY")
browserless_api_key = "4795f0e6-6128-4155-a56f-2b09cbf14afe"
crove_api_key = "31ed2630e388204290c6e198fd8c9c7d10b2109ec090c1b9565f3bfc2a42c0ba"
linkedin_api_url = "https://www.linkedin.com/jobs-guest/jobs/api"
# ---------------------------- Setting the API keys ----------------------------

# ---------------------------- LLM with Langchain ----------------------------


# Define function to generate a response
def generate_response(
    first_name,
    last_name,
    email,
    phone,
    edu1,
    linkedin_URL,
    edu1location,
    edu1course,
    edu1date,
    edu2,
    edu2location,
    edu2course,
    edu2date,
    job1,
    job1location,
    job1position,
    job1date,
    job2,
    job2location,
    job2position,
    job2date,
    desired_job,
    job_description,
):
    # Initialize the chat model with OpenAI API key
    llm = ChatOpenAI(openai_api_key=openai_api_key)
    resume_prompt = f"""
    Your name is Rezbot, and you were created for mainly one reason: writing professional resumes. You must act like a top-notch resume writer with over 20 years of experience in this domain. Here are the details of the resume:

    Person name: 
    {first_name} {last_name}
    Education:
    Studied at the {edu1} in {edu1course} from {edu1date} in {edu1location}
    Obtained a {edu2course} degree from the {edu2}  from {edu2date} in {edu2location}

    Work experience:

    Worked at {job1} company as a {job1position} from {job1date}
    Worked as a {job2position} at {job2} from {job2date}

    {first_name} is now seeking to apply for a job as a {desired_job}. You must find strengths between his skills, education, and the job description, and use them to write a powerful resume.
    Job description: {job_description}

    I want you to write the following for the resume:

    - A resume summary at least 120 words
    - 3 core competencies with explination
    - 9 technical skills
    - For each job in {first_name}'s career history, provide at least 2 quantified measures of his achievements or impact in one sentence. content generated must explain very well
    The final output should replace each value with the generated content. Put the generated content in the correct JSON field, where the field name is mentioned, such as "resume_summary", "core_competencies_1", "Technical_skill_1", "Job_1_skills_1", "Job_1_skills_2", etc. Please ensure that you do not use brackets or arrays for fields like "Job_1_skills_1" and "Job_1_skills_2". Instead, provide the values separately.    

    Here's the JSON template, phone number must be in string format :
    "template_id": "f17b9c42-f624-4f90-a876-7c6a5b61e60e",
    "name": "first_name_last_name",
    "background_mode": false,
    "response": 
        "1710497701667": {first_name},
        "1710498021979": {last_name},
        "1710508712281": {email},
        "1710508742943": {phone},
        "1710508795514": {linkedin_URL},
        "1710509102577": "resume_summary",
        "1710528829666": "core_competencies_1",
        "1710528834175": "core_competencies_2",
        "1710528850008": "core_competencies_3",
        "1710528101361": "edu1",
        "1710528162961": "edu1location",
        "1710528143880": "edu1course",
        "1710528109425": "20/03/2024",
        "1710528933896": "edu2",
        "1710528951137": "edu2location",
        "1710528987364": "edu3course",
        "1710529004648": "30/03/2024",
        "1710529715794": "job1",
        "1710529728616": "job1location",
        "1710529758192": "job1position",
        "1710529770167": "29/03/2024",
        "1710530023914": "job2",
        "1710530034695": "job2location",
        "1710530048888": "job2position",
        "1710530057718": "27/03/2024",
        "1710530088944": "Job_1_skills_1",
        "1710530096768": "Job_1_skills_2",
        "1710530226497": "Technical_skill_1",
        "1710530230911": "Technical_skill_2",
        "1710530235695": "Technical_skill_3",
        "1710530239991": "Technical_skill_4",
        "1710530248687": "Technical_skill_5",
        "1710530254678": "Technical_skill_6",
        "1710530259655": "Technical_skill_7",
        "1710530265621": "Technical_skill_8",
        "1710534118133": "Technical_skill_9"
    
        
        
        
        
    """

    # Create a prompt template with the initial context and the user's input
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                resume_prompt,
            )
        ]
    )

    # Use the prompt template to generate a chat prompt
    chat_prompt = prompt_template.format_messages()

    # Generate the response from the LLM
    response = llm.invoke(
        chat_prompt,
        max_tokens=4096,  # Set the maximum number of tokens to generate
        n=1,  # Generate 1 completion for the prompt
        stop=None,  # No specific stop sequence
    )
    # st.info(response.content)
    return response.content


# ---------------------------- LLM with Langchain ----------------------------


# ---------------------------- Cities ----------------------------
cities_in_saudi = {
    "Riyadh": "Riyadh",
    "Jeddah": "Jeddah",
    "Mecca": "Mecca",
    "Medina": "Medina",
    "Dammam": "Dammam",
    "Asir": "Asir",
    "Tabuk": "Tabuk",
    "Khobar": "Khobar",
    "Qatif": "Qatif",
    "Taif": "Taif",
    "Buraidah": "Buraidah",
    "Al-Ahsa": "Al-Ahsa",
    "Jubail": "Jubail",
    "Hail": "Hail",
    "Al-Kharj": "Al-Kharj",
    "Yanbu": "Yanbu",
    "Abha": "Abha",
    "Najran": "Najran",
    "Jizan": "Jizan",
    "Sakaka": "Sakaka",
    "Al-Baha": "Al-Baha",
    "Eastern Province": "Eastern Province",
    "All locations": "Saudi Arabia",
}

selected_cities = []


# ---------------------------- Cities ----------------------------


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


def jobs_display(
    job_data,
    first_name,
    last_name,
    email,
    phone,
    linkedin_URL,
    edu1,
    edu1location,
    edu1course,
    edu1date,
    edu2,
    edu2location,
    edu2course,
    edu2date,
    job1,
    job1location,
    job1position,
    job1date,
    job2,
    job2location,
    job2position,
    job2date,
    desired_job,
):
    # Layout Parameters
    num_columns_per_row = 3

    # Create Columns
    columns = st.columns(num_columns_per_row)

    for index, job in enumerate(job_data):
        column_index = index % num_columns_per_row
        with columns[column_index]:
            create_job_div(
                job,
                index,
                first_name,
                last_name,
                email,
                phone,
                linkedin_URL,
                edu1,
                edu1location,
                edu1course,
                edu1date,
                edu2,
                edu2location,
                edu2course,
                edu2date,
                job1,
                job1location,
                job1position,
                job1date,
                job2,
                job2location,
                job2position,
                job2date,
                desired_job,
            )


def create_job_div(
    job,
    index,
    first_name,
    last_name,
    email,
    phone,
    linkedin_URL,
    edu1,
    edu1location,
    edu1course,
    edu1date,
    edu2,
    edu2location,
    edu2course,
    edu2date,
    job1,
    job1location,
    job1position,
    job1date,
    job2,
    job2location,
    job2position,
    job2date,
    desired_job,
):
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
            job_description = job["jDetails"]
            st.write(job_description)
            with st.spinner("Generating the resume..."):
                # Get OpenAI JSON object
                jjson = generate_response(
                    first_name,
                    last_name,
                    email,
                    phone,
                    linkedin_URL,
                    edu1,
                    edu1location,
                    edu1course,
                    edu1date,
                    edu2,
                    edu2location,
                    edu2course,
                    edu2date,
                    job1,
                    job1location,
                    job1position,
                    job1date,
                    job2,
                    job2location,
                    job2position,
                    job2date,
                    desired_job,
                    job_description,
                )

                # This ensures the spinner shows while the function is running
                success, result = generate_resume_pdf(jjson)
                if success:
                    st.success("Resume Generated!")
                    st.markdown(
                        f'<a href="{result}" target="_blank">Download Resume</a>',
                        unsafe_allow_html=True,
                    )  # Display the PDF file
                else:
                    st.error(result)  # Display the error message


# ---------------------------- Split Jobs by 3 columns and styling them using CSS ----------------------------


# ---------------------------- Fetching Jobs and crawling their data ----------------------------
async def fetch_jobs(url):
    browser = await pyppeteer.launcher.connect(
        browserWSEndpoint="wss://chrome.browserless.io?token=" + browserless_api_key
    )
    page = await browser.newPage()
    await page.setUserAgent(customUA)
    await page.goto(url)
    cookies = await page.cookies()
    cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies}

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
        with requests.Session() as s:
            response = s.get(
                job_details["Job URL"], cookies=cookies_dict, headers=headers
            )
            soup = BeautifulSoup(response.content, features="lxml")
            job_description = soup.select(
                ".show-more-less-html__markup.relative.overflow-hidden"
            )
            job_details["jDetails"] = clean_text(
                " ".join(element.get_text() for element in job_description)
            )

        alljobs.append(job_details)

    await browser.close()
    return alljobs


# ---------------------------- Fetching Jobs and crawling their data ----------------------------


# ---------------------------- Generate PDF ----------------------------


def generate_resume_pdf(jjson):

    url = "https://v2.api.crove.app/api/integrations/external/helpers/generate-pdf-from-template/"  # Replace this with the actual API URL

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": crove_api_key,
    }

    # if linkedin_URL:  # This checks if linkedin_URL is neither empty nor None
    #     json_body["response"]["1710508795514"] = linkedin_URL
    json_data = json.loads(jjson)
    response = requests.post(url, headers=headers, json=json_data)
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()
        pdfFile = json_response["latest_pdf"]
        return True, pdfFile  # Return a tuple indicating success and the PDF file
    else:
        return (
            False,
            f"Failed to make a request. Status code: {response.status_code}",
        )  # Indicate failure and the status code


# ---------------------------- Generate PDF ----------------------------
# ---------------------------- Linkedin URL ----------------------------
def linkedinURL(desired_job, selected_cities_str):
    url = (
        linkedin_api_url
        + "/seeMoreJobPostings/search?keywords="
        + desired_job
        + "&location="
        + selected_cities_str
        + "&pageNum=0&original_referer="
    )
    return url


# ---------------------------- Linkedin URL ----------------------------


async def main():
    st.set_page_config(page_title="RezBot", page_icon="📝")
    st.title("RezBot")

    with st.sidebar:
        selected_cities_str = ""
        st.write("Choose your work locations")
        with st.popover("Location"):
            st.markdown("Choose your preferred work locations")
            for city_name, city_value in cities_in_saudi.items():
                if st.checkbox(city_name, key=city_value):
                    selected_cities.append(city_value)
                    selected_cities_str = "&".join(selected_cities)
        st.write("Selected location(s):", selected_cities_str)

        st.write("Please specify the job title you are applying for.")
        desired_job = st.text_input("Job title", "", placeholder="Data Engineer")

        fetch_jobs_clicked = st.button("Fetch Jobs", type="primary")

        st.write("Lets gather basic info of you")
        c1, c2 = st.columns(2)
        with c1:
            first_name = st.text_input("First name", "", placeholder="Mohammed")
        with c2:
            last_name = st.text_input("Last name", "", placeholder="Abdulatef")

        linkedin_URL = st.text_input(
            "Linkedin/Website URL",
            "",
            placeholder="https://www.linkedin.com/in/[username]/",
        )

        c4, c5 = st.columns(2)
        with c4:
            email = st.text_input("Email", "", placeholder="Mohammed@gmail.com")
        with c5:
            phone = st.text_input("Phone", "", placeholder="0597593221")

        st.write("Please fill all the details")
        c6, c7, c8, c9 = st.columns(4)
        with c6:
            edu1 = st.text_input(
                "University name", "", placeholder="University of ....", key="ixk"
            )
        with c7:
            edu1location = st.text_input(
                "Location", "", placeholder="Dammam", key="f2s"
            )
        with c8:
            edu1course = st.text_input(
                "Degree", "", placeholder="Environmental engineer", key="d8b5"
            )
        with c9:
            edu1date = st.text_input(
                "Date duration", "", placeholder="2015-2020", key="ixkb5"
            )

        c10, c11, c12, c13 = st.columns(4)
        with c10:
            edu2 = st.text_input(
                "University name", "", placeholder="University of ...."
            )
        with c11:
            edu2location = st.text_input("Location", "", placeholder="UK")
        with c12:
            edu2course = st.text_input("Master", "", placeholder="No-code AI")
        with c13:
            edu2date = st.text_input("Date duration", "", placeholder="2020-2022")

        c14, c15, c16, c17 = st.columns(4)
        with c14:
            job1 = st.text_input("Company name", "", placeholder="Aramco", key="c0k")
        with c15:
            job1location = st.text_input(
                "Location", "", placeholder="Jeddah", key="psv"
            )
        with c16:
            job1position = st.text_input(
                "Position", "", placeholder="Data Analyst", key="x3dv"
            )
        with c17:
            job1date = st.text_input(
                "Duration", "", placeholder="2021-2022", key="v3vvv"
            )

        c18, c19, c20, c21 = st.columns(4)
        with c18:
            job2 = st.text_input("Company name", "", placeholder="Aramco", key="cvew")
        with c19:
            job2location = st.text_input(
                "Location", "", placeholder="Jeddah", key="dkb3"
            )
        with c20:
            job2position = st.text_input(
                "Position", "", placeholder="Data Engineer", key="xx74csp"
            )
        with c21:
            job2date = st.text_input(
                "Duration", "", placeholder="2020-2021", key="xmso"
            )

    if fetch_jobs_clicked:
        # Check if the required fields are not empty
        if not all([desired_job, selected_cities_str]):
            st.error("Job title and locations required")
        else:
            with st.spinner("Fetching..."):
                job_data = await fetch_jobs(
                    linkedinURL(desired_job, selected_cities_str)
                )
                st.success("Jobs Fetched!")
                if job_data:
                    # st.info(job_data)
                    html_code = jobs_display(
                        job_data,
                        first_name,
                        last_name,
                        email,
                        phone,
                        linkedin_URL,
                        edu1,
                        edu1location,
                        edu1course,
                        edu1date,
                        edu2,
                        edu2location,
                        edu2course,
                        edu2date,
                        job1,
                        job1location,
                        job1position,
                        job1date,
                        job2,
                        job2location,
                        job2position,
                        job2date,
                        desired_job,
                    )
                else:
                    st.write("No jobs found.")


if __name__ == "__main__":
    asyncio.run(main())


# ---------------------------- Inject custom CSS to style the page and especially the modal ----------------------------
st.markdown(
    """
<style>

[data-testid="stHorizontalBlock"] {
    /*display: flex;
    align-items: end;*/
}
body [data-testid="stVerticalBlockBorderWrapper"] div[data-modal-container='true'] > div:first-child > div:first-child {
    top: 10%;
    left: 50%;
    transform: translate(-50%);
    position: fixed;
    width: 50% !important;
    min-width: 350px;
    max-width: 750px;
}

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
# ---------------------------- Inject custom CSS to style the page and especially the modal ----------------------------
