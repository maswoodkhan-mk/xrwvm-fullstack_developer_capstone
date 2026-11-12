import os
import requests
from dotenv import load_dotenv

load_dotenv()
backend_url = os.getenv("backend_url", default="http://localhost:3030")
sentiment_analyzer_url = os.getenv("sentiment_analyzer_url", default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    try:
        response = requests.get(f"{backend_url.rstrip(chr(47))}/{endpoint.lstrip(chr(47))}", params=kwargs, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print(f"Backend GET failed: {error}")
        return None

def analyze_review_sentiments(text):
    try:
        response = requests.get(f"{sentiment_analyzer_url.rstrip(chr(47))}/analyze/{text}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print(f"Sentiment request failed: {error}")
        return None

def post_review(data_dict):
    try:
        response = requests.post(f"{backend_url.rstrip(chr(47))}/insert_review", json=data_dict, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print(f"Backend POST failed: {error}")
        return None
