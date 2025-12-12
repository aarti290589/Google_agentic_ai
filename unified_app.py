import streamlit as st
import os
from main_workflow import run_agentic_analysis
from google.cloud import bigquery

def fetch_bigquery_data(settings, restaurant, location):
    client = bigquery.Client(project=settings.VERTEX_AI_PROJECT_ID)
    table_id = f"{settings.VERTEX_AI_PROJECT_ID}.{settings.BIGQUERY_DATASET}.review_analysis"
    query = f'''
        SELECT review_text, sentiment, aspect, recommendation, source
        FROM `{table_id}`
        WHERE restaurant_name = @restaurant AND location = @location
        ORDER BY sentiment, aspect
    '''
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("restaurant", "STRING", restaurant),
            bigquery.ScalarQueryParameter("location", "STRING", location),
        ]
    )
    return client.query(query, job_config=job_config).to_dataframe()

def main():
    from config.settings import settings
    st.set_page_config(page_title="Insight2Action: Unified App", layout="wide")
    st.title("Insight2Action: Restaurant Review Analyzer & Dashboard")
    st.write("Enter a restaurant name and location to analyze reviews with Gemini AI and view results below.")

    restaurant = st.text_input("Restaurant Name", value="")
    location = st.text_input("Location (City, State)", value="")
    run_button = st.button("Analyze Reviews")

    if 'analysis_ran' not in st.session_state:
        st.session_state['analysis_ran'] = False

    if run_button and restaurant and location:
        os.environ['PLACE_NAME'] = restaurant
        os.environ['LOCATION'] = location
        from importlib import reload
        import config.settings
        reload(config.settings)
        settings = config.settings.settings
        with st.spinner("Running analysis with Gemini AI..."):
            results = run_agentic_analysis(settings)
        st.success("Analysis complete! Dashboard updated below.")
        st.session_state['analysis_ran'] = True

    if st.session_state['analysis_ran']:
        st.subheader("Dashboard: Review Analysis Results")
        data = fetch_bigquery_data(settings, restaurant, location)
        if data.empty:
            st.warning("No review analysis data found in BigQuery for this restaurant/location.")
        else:
            import altair as alt
            st.write(f"Total reviews analyzed: {len(data)}")
            st.dataframe(data)
            st.subheader("Sentiment Distribution")
            sentiment_counts = data['sentiment'].value_counts().reset_index()
            sentiment_counts.columns = ['sentiment', 'count']
            sentiment_chart = alt.Chart(sentiment_counts).mark_bar().encode(
                x=alt.X('count:Q', title='Count'),
                y=alt.Y('sentiment:N', sort='-x', title='Sentiment'),
                color=alt.Color('sentiment:N'),
                tooltip=['sentiment', 'count']
            ).properties(width=600, height=200)
            st.altair_chart(sentiment_chart, use_container_width=True)
            st.subheader("Top Aspects Mentioned")
            aspect_counts = data['aspect'].value_counts().head(10).reset_index()
            aspect_counts.columns = ['aspect', 'count']
            aspect_chart = alt.Chart(aspect_counts).mark_bar().encode(
                x=alt.X('count:Q', title='Count'),
                y=alt.Y('aspect:N', sort='-x', title='Aspect'),
                color=alt.Color('aspect:N'),
                tooltip=['aspect', 'count']
            ).properties(width=600, height=300)
            st.altair_chart(aspect_chart, use_container_width=True)
            st.subheader("Sample Recommendations")
            for i, row in data.head(5).iterrows():
                st.markdown(f"**Review:** {row['review_text']}")
                st.markdown(f"- Sentiment: {row['sentiment']}")
                st.markdown(f"- Aspect: {row['aspect']}")
                st.markdown(f"- Recommendations: {row['recommendation']}")
                st.markdown(f"- Source: {row['source']}")
                st.markdown("---")
    else:
        st.info("Run an analysis to see the dashboard.")

if __name__ == "__main__":
    main()
