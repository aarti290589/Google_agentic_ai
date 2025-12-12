# data_processing/data_writer.py

from google.cloud import bigquery
from config.settings import settings

def list_bigquery_tables():
    client = bigquery.Client(project=settings.VERTEX_AI_PROJECT_ID)
    dataset_ref = f"{settings.VERTEX_AI_PROJECT_ID}.{settings.BIGQUERY_DATASET}"
    print(f"[DEBUG] Listing tables in dataset: {dataset_ref}")
    tables = list(client.list_tables(dataset_ref))
    for table in tables:
        print(f"[DEBUG] Found table: {table.table_id}")

def write_to_bigquery(data):
    print("[DATA WRITER] Writing data to BigQuery...")
    client = bigquery.Client(project=settings.VERTEX_AI_PROJECT_ID)
    table_id = f"{settings.VERTEX_AI_PROJECT_ID}.{settings.BIGQUERY_DATASET}.review_analysis"
    print(f"[DEBUG] Writing to table: {table_id}")
    errors = client.insert_rows_json(table_id, data)
    if errors:
        print(f"[ERROR] Failed to write to BigQuery: {errors}")
    else:
        print("[DATA WRITER] Data written to BigQuery successfully.")
