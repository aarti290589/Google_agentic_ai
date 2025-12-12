import os
import requests
from config.settings import settings
from vertexai import init
from vertexai.preview.generative_models import GenerativeModel

def call_gemini_api(prompt, project_id=None):
    """
    Calls the Gemini 2.5 Pro (Vertex AI) API for LLM-based review analysis.
    """
    project = project_id or settings.VERTEX_AI_PROJECT_ID
    location = "us-central1"  # or your region
    init(project=project, location=location)
    model = GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(prompt)
    return response.text

def fetch_reviews(place_name, source='google', location=None):
    print(f"[DATA INGESTION] Fetching reviews for {place_name} from {source}...")
    if source == 'google':
        api_key = settings.GOOGLE_API_KEY
        # Step 1: Get Place ID
        search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            'input': f"{place_name} {location}" if location else place_name,
            'inputtype': 'textquery',
            'fields': 'place_id',
            'key': api_key
        }
        resp = requests.get(search_url, params=params)
        place_id = resp.json().get('candidates', [{}])[0].get('place_id')
        if not place_id:
            print("[ERROR] Place ID not found.")
            return []
        # Step 2: Get Reviews
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': place_id,
            'fields': 'review',
            'key': api_key
        }
        resp = requests.get(details_url, params=params)
        reviews = resp.json().get('result', {}).get('reviews', [])
        return reviews
    else:
        print(f'[ERROR] Unknown review source: {source}')
        return []
