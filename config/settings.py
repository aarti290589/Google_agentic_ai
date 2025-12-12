import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    VERTEX_AI_PROJECT_ID = os.getenv('VERTEX_AI_PROJECT_ID')
    GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
    BIGQUERY_DATASET = os.getenv('BIGQUERY_DATASET')
    PLACE_NAME = os.getenv('PLACE_NAME')
    LOCATION = os.getenv('LOCATION')

settings = Settings()
