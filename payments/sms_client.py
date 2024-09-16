import urllib.parse
from typing import List

import requests
from django.conf import settings


# Function to send SMS using Deywuro API (GET request)
def send_sms_get(destination: List[str], message: str) -> dict:
    base_url = "https://deywuro.com/api/sms/"

    # Loading credentials from the .env file
    username = settings.DEYWURO_USERNAME
    password = settings.DEYWURO_PASSWORD
    source = settings.DEYWURO_SOURCE

    # Prepare the query parameters
    params = {
        "username": username,
        "password": password,
        "destination": ",".join(destination),  # Join numbers with commas
        "source": source,
        "message": message,
    }

    # Encode the parameters for URL
    query_string = urllib.parse.urlencode(params)
    request_url = f"{base_url}?{query_string}"

    try:
        response = requests.get(request_url)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()  # Return the response in JSON format
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"Other error occurred: {err}"}
