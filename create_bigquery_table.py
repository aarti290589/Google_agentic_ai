from google.cloud import bigquery

project_id = "teamagenticai"
dataset_id = "restaurant_reviews"
table_id = "review_analysis"

client = bigquery.Client(project=project_id)
table_ref = f"{project_id}.{dataset_id}.{table_id}"

schema = [
    bigquery.SchemaField("review_text", "STRING"),
    bigquery.SchemaField("sentiment", "STRING"),
    bigquery.SchemaField("aspect", "STRING"),
    bigquery.SchemaField("recommendation", "STRING", mode="REPEATED"),
    bigquery.SchemaField("source", "STRING"),
    bigquery.SchemaField("restaurant_name", "STRING"),
    bigquery.SchemaField("location", "STRING"),
]

table = bigquery.Table(table_ref, schema=schema)
try:
    client.get_table(table_ref)
    print("Table already exists.")
except Exception:
    table = client.create_table(table)
    print(f"Created table {table_ref}")
