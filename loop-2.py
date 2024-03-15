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

import os


from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# from streamlit_chat import message


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


# echo "export OPENAI_API_KEY='sk-xxxxxxxxxx'" >> ~/.zshrc
# Setting the API key
openai_api_key = os.environ["OPENAI_API_KEY"]


# ---------------------------- LLM with Langchain ----------------------------


# Define function to generate a response
def generate_response(input_text):
    # Initialize the chat model with OpenAI API key
    llm = ChatOpenAI(openai_api_key=openai_api_key)

    # Create a prompt template with the initial context and the user's input
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are RezBot, a bot that aims to help graduate students find their job.",
            ),
            ("user", input_text),
        ]
    )

    # Use the prompt template to generate a chat prompt
    chat_prompt = prompt_template.format_messages()

    # Generate the response from the LLM
    response = llm.invoke(
        chat_prompt,
        max_tokens=100,  # Set the maximum number of tokens to generate
        n=1,  # Generate 1 completion for the prompt
        stop=None,  # No specific stop sequence
    )
    st.info(response.content)
    return response


# ---------------------------- LLM with Langchain ----------------------------


with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "Who are you and what you do?",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)

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


# ---------------------------- Generate HTML to display job results ----------------------------
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
    return html_strs


# ---------------------------- Generate HTML to display job results ----------------------------

c1, c2, c3 = st.columns(3)
with c1:
    first_name = st.text_input("First name", "", placeholder="Mohammed")
with c2:
    last_name = st.text_input("Last name", "", placeholder="Abdulatef")
with c3:
    linkedin_URL = st.text_input(
        "Linkedin/Website URL",
        "",
        placeholder="https://www.linkedin.com/in/[username]/",
    )

c4, c5, c6 = st.columns(3)
with c4:
    email = st.text_input("Email", "", placeholder="Mohammed@gmail.com")
with c5:
    phone = st.text_input("Phone", "", placeholder="0597593221")
with c6:
    with st.popover("Location"):
        st.markdown("Choose your preferred work locations")
        for city_name, city_value in cities_in_saudi.items():
            if st.checkbox(city_name, key=city_value):
                selected_cities.append(city_value)


# st.write("Your name:", name)


# ---------------------------- Generate PDF ----------------------------


def generate_resume_pdf(first_name, last_name, linkedin_URL, email, phone):
    full_name = first_name + "_" + last_name
    url = "https://v2.api.crove.app/api/integrations/external/helpers/generate-pdf-from-template/"  # Replace this with the actual API URL

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": os.environ["CROVE_API_KEY"],
    }

    json_body = {
        "template_id": "f17b9c42-f624-4f90-a876-7c6a5b61e60e",
        "name": full_name,
        "background_mode": False,
        "response": {
            "1710497701667": first_name,
            "1710498021979": last_name,
            "1710508712281": email,
            "1710508742943": phone,
            "1710509102577": "about",
            "1710528829666": "core1",
            "1710528834175": "core2",
            "1710528850008": "core3",
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
            "1710530088944": "Job1skills1 \n new line \n ldsif sd\n gfgg \t dsfds \r bbbbb",
            "1710530096768": "Job1skills2",
            "1710530226497": "skill1",
            "1710530230911": "Skill2",
            "1710530235695": "Skill3",
            "1710530239991": "Skill4",
            "1710530248687": "Skill5",
            "1710530254678": "Skill6",
            "1710530259655": "Skill7",
            "1710530265621": "Skill8",
            "1710534118133": "Skill9",
        },
    }
    if linkedin_URL:  # This checks if linkedin_URL is neither empty nor None
        json_body["response"]["1710508795514"] = linkedin_URL

    response = requests.post(url, headers=headers, json=json_body)
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


if st.button("Build Resume", type="primary"):
    # Check if the required fields are not empty
    if not all([first_name, last_name, email, phone]):
        st.error("Please fill in all required fields.")
    else:
        with st.spinner(
            "Generating the resume..."
        ):  # This ensures the spinner shows while the function is running
            success, result = generate_resume_pdf(
                first_name, last_name, linkedin_URL, email, phone
            )
            if success:
                st.success("Resume Generated!")
                st.markdown(
                    f'<a href="{result}" target="_blank">Download Resume</a>',
                    unsafe_allow_html=True,
                )  # Display the PDF file
            else:
                st.error(result)  # Display the error message

# ---------------------------- Generate PDF ----------------------------


json_data = [
    {
        "Title": "Human 1 &!",
        "Company": "Helmerich & Payne",
        "Location": "Al Khobar, Eastern, Saudi Arabia",
        "Job URL": "https://sa.linkedin.com/jobs/view/human-resources-officer-at-helmerich-payne-3842068224?position=1&pageNum=0&refId=QgU2InY9bJUn%2BVK2ZMXdUg%3D%3D&trackingId=ysUV%2FNWbHimtbPcPGbl4NA%3D%3D&trk=public_jobs_jserp-result_search-card",
    },
    {
        "Title": "Human 2 &!",
        "Company": "ssss & ccc",
        "Location": "Al Khobar, Eastern, Saudi Arabia",
        "Job URL": "https://sa.linkedin.com/jobs/view/human-resources-officer-at-helmerich-payne-3842068224?position=1&pageNum=0&refId=QgU2InY9bJUn%2BVK2ZMXdUg%3D%3D&trackingId=ysUV%2FNWbHimtbPcPGbl4NA%3D%3D&trk=public_jobs_jserp-result_search-card",
    },
    {
        "Title": "Human 3&!",
        "Company": "fdsfdsf & dsfsdf",
        "Location": "Al Khobar, Eastern, Saudi Arabia",
        "Job URL": "https://sa.linkedin.com/jobs/view/human-resources-officer-at-helmerich-payne-3842068224?position=1&pageNum=0&refId=QgU2InY9bJUn%2BVK2ZMXdUg%3D%3D&trackingId=ysUV%2FNWbHimtbPcPGbl4NA%3D%3D&trk=public_jobs_jserp-result_search-card",
    },
    {
        "Title": "Human 4&!",
        "Company": "4234234 & vcxvxcv",
        "Location": "Al Khobar, Eastern, Saudi Arabia",
        "Job URL": "https://sa.linkedin.com/jobs/view/human-resources-officer-at-helmerich-payne-3842068224?position=1&pageNum=0&refId=QgU2InY9bJUn%2BVK2ZMXdUg%3D%3D&trackingId=ysUV%2FNWbHimtbPcPGbl4NA%3D%3D&trk=public_jobs_jserp-result_search-card",
    },
    {
        "Title": "Human 5&!",
        "Company": "234fdsd & vsvsdv",
        "Location": "Al Khobar, Eastern, Saudi Arabia",
        "Job URL": "https://sa.linkedin.com/jobs/view/human-resources-officer-at-helmerich-payne-3842068224?position=1&pageNum=0&refId=QgU2InY9bJUn%2BVK2ZMXdUg%3D%3D&trackingId=ysUV%2FNWbHimtbPcPGbl4NA%3D%3D&trk=public_jobs_jserp-result_search-card",
    },
    {
        "Title": "Human 5&!",
        "Company": "234fdsd & vsvsdv",
        "Location": "Al Khobar, Eastern, Saudi Arabia",
        "Job URL": "https://sa.linkedin.com/jobs/view/human-resources-officer-at-helmerich-payne-3842068224?position=1&pageNum=0&refId=QgU2InY9bJUn%2BVK2ZMXdUg%3D%3D&trackingId=ysUV%2FNWbHimtbPcPGbl4NA%3D%3D&trk=public_jobs_jserp-result_search-card",
    },
    {
        "Title": "Human 5&!",
        "Company": "234fdsd & vsvsdv",
        "Location": "Al Khobar, Eastern, Saudi Arabia",
        "Job URL": "https://sa.linkedin.com/jobs/view/human-resources-officer-at-helmerich-payne-3842068224?position=1&pageNum=0&refId=QgU2InY9bJUn%2BVK2ZMXdUg%3D%3D&trackingId=ysUV%2FNWbHimtbPcPGbl4NA%3D%3D&trk=public_jobs_jserp-result_search-card",
    },
    {
        "Title": "Human 5&!",
        "Company": "234fdsd & vsvsdv",
        "Location": "Al Khobar, Eastern, Saudi Arabia",
        "Job URL": "https://sa.linkedin.com/jobs/view/human-resources-officer-at-helmerich-payne-3842068224?position=1&pageNum=0&refId=QgU2InY9bJUn%2BVK2ZMXdUg%3D%3D&trackingId=ysUV%2FNWbHimtbPcPGbl4NA%3D%3D&trk=public_jobs_jserp-result_search-card",
    },
    {
        "Title": "Human 5&!",
        "Company": "234fdsd & vsvsdv",
        "Location": "Al Khobar, Eastern, Saudi Arabia",
        "Job URL": "https://sa.linkedin.com/jobs/view/human-resources-officer-at-helmerich-payne-3842068224?position=1&pageNum=0&refId=QgU2InY9bJUn%2BVK2ZMXdUg%3D%3D&trackingId=ysUV%2FNWbHimtbPcPGbl4NA%3D%3D&trk=public_jobs_jserp-result_search-card",
    },
]


def create_view_button(job, index):
    # Unique key for each button based on job index
    button_key = f"view_button_{index}"

    # Instantiate the Modal object
    # modal = Modal(title=f"job['Title']", key=f"modal_key_{index}")
    modal = Modal(title=job["Title"], key=f"modal_key_{index}")
    # Button to open the modal
    if st.button("View Title", key=button_key):
        modal.open()

    if modal.is_open():
        with modal.container():
            st.write("Job Details")

            st.write("Some fancy text")
            value = st.checkbox("Check me")
            st.write(f"Checkbox checked: {value}")
            if st.button("Close", key=f"close_modal_{index}"):
                modal.close()


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
        create_view_button(job, index)


# Layout Parameters
num_columns_per_row = 3

# Create Columns
columns = st.columns(num_columns_per_row)

# Assuming you have a variable `num_columns_per_row` defined
# and a Streamlit columns setup `columns`
for index, job in enumerate(json_data):
    column_index = index % num_columns_per_row
    with columns[column_index]:
        create_job_div(job, index)


# Inject custom CSS to center the modal
st.markdown(
    """
<style>

[data-testid="stHorizontalBlock"] {
    display: flex;
    align-items: end;
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
