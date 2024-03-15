import streamlit as st
import streamlit.components.v1 as components
from streamlit_modal import Modal
import uuid


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
]

# Layout Parameters
num_columns_per_row = 3

# Create Columns
columns = st.columns(num_columns_per_row)


def create_job_div(job, index):
    with st.container():
        st.markdown(
            f"""
            <div class="ops">
                <h2>{job['Title']}</h2>  
                <p>{job['Company']}</p>
                <p>{job['Location']}</p>
                <a href="{job['Job URL']}" target="_blank">Job Details</a>
                {create_view_button(job, index)}  
            </div>""",
            unsafe_allow_html=True,
        )


def create_view_button(job, index):
    button_id = f"view_button_{job['Title'].replace(' ', '_')}_{index}"
    view_button = st.button("View", key=button_id)

    if view_button:  # Key change!
        show_modal(job)  # Call show_modal only if the button is clicked


def show_modal(job):

    if "job_modal" not in st.session_state:
        # Create the modal only if it doesn't exist
        st.session_state["job_modal"] = Modal(
            job["Title"], key=f"job-modal_{job['Title'].replace(' ', '_')}"
        )

    modal = st.session_state["job_modal"]  # Retrieve the existing modal

    st.session_state["modal_open"] = True  # Signal to open the modal

    with modal.container():
        st.write(f"**Company:** {job['Company']}")


# Generate Divs
for index, job in enumerate(json_data):
    column_index = index % num_columns_per_row
    with columns[column_index]:
        create_job_div(job, index)

# Modal Handling
if st.session_state:
    button_id = st.session_state.pop("button_id", None)  # Get pressed button's ID
    if button_id:
        for job in json_data:
            if f"view_button_{job['Title']}" == button_id:
                show_modal(
                    {
                        "title": job["Title"],
                        "company": job["Company"],
                        "location": job["Location"],
                        "url": job["Job URL"],
                    }
                )
                break  # Exit loop once the job is found


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


with st.popover("Open popover"):
    st.markdown("Hello World 👋")
    name = st.text_input("What's your name?")

st.write("Your name:", name)
