import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrape information from linkedin profiles,
    Manually scrape the information from the linkedin profile"""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/RAHULREDDYYSR/4781c692be69f3991948de33e58fde7a/raw/140b9b4c82ec557febcd57ea03667436ade3bdb9/gistfile1.txt"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(api_endpoint, params=params, timeout=10)

    data = response.json().get("person")

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None) and k not in ["certifications"]
    }
    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/nithin-kumar-k-a-b112502b1/"
        )
    )
