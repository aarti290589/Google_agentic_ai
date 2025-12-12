import streamlit as st
from google.cloud import bigquery
from config.settings import settings

st.set_page_config(page_title="Insight2Action Dashboard", layout="wide")
st.title("Insight2Action: Review Analysis Dashboard")

# Connect to BigQuery and fetch data
def fetch_bigquery_data():
    client = bigquery.Client(project=settings.VERTEX_AI_PROJECT_ID)
    table_id = f"{settings.VERTEX_AI_PROJECT_ID}.{settings.BIGQUERY_DATASET}.review_analysis"
    query = f"""
        SELECT review_text, sentiment, aspect, recommendation, source
        FROM `{table_id}`
        ORDER BY sentiment, aspect
    """
    return client.query(query).to_dataframe()

data = fetch_bigquery_data()

if data.empty:
    st.warning("No review analysis data found in BigQuery.")
else:
    st.write(f"Total reviews analyzed: {len(data)}")
    st.dataframe(data)

    st.subheader("Sentiment Distribution")
    sentiment_counts = data['sentiment'].value_counts()
    st.bar_chart(sentiment_counts)

    st.subheader("Top Aspects Mentioned")
    aspect_counts = data['aspect'].value_counts().head(10)
    st.bar_chart(aspect_counts)

    st.subheader("Sample Recommendations")
    for i, row in data.head(5).iterrows():
        st.markdown(f"**Review:** {row['review_text']}")
        st.markdown(f"- Sentiment: {row['sentiment']}")
        st.markdown(f"- Aspect: {row['aspect']}")
        st.markdown(f"- Recommendations: {row['recommendation']}")
        st.markdown(f"- Source: {row['source']}")
        st.markdown("---")
