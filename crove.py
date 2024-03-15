import requests
import json


def generate_resume_pdf():
    url = "https://v2.api.crove.app/api/integrations/external/helpers/generate-pdf-from-template/"  # Replace this with the actual API URL

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": "31ed2630e388204290c6e198fd8c9c7d10b2109ec090c1b9565f3bfc2a42c0ba",
    }

    json_body = {
        "template_id": "f17b9c42-f624-4f90-a876-7c6a5b61e60e",
        "name": "test-cix",
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
    print(response.json)
    print("------------")
    response_json = json.dumps(response)
    print(response_json[0].get("latest_pdf", None))
    # if response.status_code == 200:
    #     # Parse the JSON response
    #     json_response = response.json()
    #     # Assuming the JSON response is a list of dictionaries and you're interested in the first item
    #     if json_response and isinstance(json_response, list) and len(json_response) > 0:
    #         print(json_response)
    #         latest_pdf = json_response[0].get("latest_pdf", None)
    #         print(latest_pdf)
    #         if latest_pdf is not None:
    #             print(f"The value of latest_pdf is: {latest_pdf}")

    #         else:
    #             print("The key 'latest_pdf' was not found in the response.")
    #     else:
    #         print(
    #             "The response JSON is not in the expected format (a list of dictionaries)."
    #         )
    # else:
    #     print(f"Failed to make a request. Status code: {response.status_code}")


# Call the function
generate_resume_pdf()
