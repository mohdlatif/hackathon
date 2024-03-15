import requests
import streamlit as st
import streamlit.components.v1 as components
from streamlit_modal import Modal

import os

# import openai
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# from streamlit_chat import message

# Setting the API key
openai_api_key = os.environ["OPENAI_API_KEY"]


# Define your function to generate a response
def generate_response(input_text):
    # Initialize the chat model with your OpenAI API key
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


with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "Who are you and what you do?",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)


c1, c2, c3 = st.columns(3)
with c1:
    first_name = st.text_input("First name", "", placeholder="Mohammed")
with c2:
    last_name = st.text_input("Last name", "", placeholder="Abdulatef")
with c3:
    linkedin_URL = st.text_input(
        "Linkedin URL", "", placeholder="https://www.linkedin.com/in/[username]/"
    )

c3, c4, c5 = st.columns(3)
with c3:
    email = st.text_input("Email", "", placeholder="Mohammed@gmail.com")
with c4:
    phone = st.text_input("Phone", "", placeholder="0597593221")
with c5:
    with st.popover("Location"):
        st.markdown("Hello World 👋")
        name = st.text_input("What's your name?")


st.write("Your name:", name)

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
    "All Saudia": "Saudi Arabia",
}

selected_cities = []


for city_name, city_value in cities_in_saudi.items():
    if st.checkbox(city_name, key=city_value):
        selected_cities.append(city_value)

st.write("loca:", selected_cities)
# ---------------------------- Cities ----------------------------


# ---------------------------- Generate PDF ----------------------------


def generate_resume_pdf():
    url = "https://v2.api.crove.app/api/integrations/external/helpers/generate-pdf-from-template/"  # Replace this with the actual API URL

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": "31ed2630e388204290c6e198fd8c9c7d10b2109ec090c1b9565f3bfc2a42c0ba",
    }

    json_body = {
        "template_id": "f17b9c42-f624-4f90-a876-7c6a5b61e60e",
        "name": "tt-f2",
        "background_mode": False,
        "response": {
            "1710497701667": "first_name",
            "1710498021979": "last_name",
            "1710508712281": "email@gmail.com",
            "1710508742943": "0116230084",
            "1710508795514": "https://linkedin.com/ff",
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

    response = requests.post(url, headers=headers, json=json_body)

    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()

        # Assuming the JSON response is a list of dictionaries and you're interested in the first item
        if json_response and isinstance(json_response, list) and len(json_response) > 0:
            st.write(json_response)
            latest_pdf = json_response[0].get("latest_pdf", None)
            st.write(latest_pdf)
            if latest_pdf is not None:
                print(f"The value of latest_pdf is: {latest_pdf}")
                st.write(latest_pdf)
            else:
                print("The key 'latest_pdf' was not found in the response.")
        else:
            print(
                "The response JSON is not in the expected format (a list of dictionaries)."
            )
    else:
        print(f"Failed to make a request. Status code: {response.status_code}")


# Call the function
generate_resume_pdf()


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
