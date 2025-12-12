import streamlit as st
import os
from main_workflow import run_agentic_analysis

def main():
    # Import settings inside the function to avoid UnboundLocalError
    from config.settings import settings
    st.title("Insight2Action: Restaurant Review Analyzer")
    st.write("Enter a restaurant name and location to analyze reviews with Gemini AI.")

    restaurant = st.text_input("Restaurant Name", value=settings.PLACE_NAME or "")
    location = st.text_input("Location (City, State)", value=settings.LOCATION or "")
    run_button = st.button("Analyze Reviews")

    if run_button and restaurant and location:
        # Update environment variables for dynamic input
        os.environ['PLACE_NAME'] = restaurant
        os.environ['LOCATION'] = location
        # Reload settings to pick up new env vars
        from importlib import reload
        import config.settings
        reload(config.settings)
        settings = config.settings.settings
        # Run the analysis
        with st.spinner("Running analysis..."):
            results = run_agentic_analysis(settings)
        st.success("Analysis complete!")
        st.write("## Results:")
        if results:
            for r in results:
                st.markdown(f"**Review:** {r['review_text']}")
                st.markdown(f"- Sentiment: {r['sentiment']}")
                st.markdown(f"- Aspect: {r['aspect']}")
                st.markdown(f"- Recommendations: {', '.join(r['recommendation']) if isinstance(r['recommendation'], list) else r['recommendation']}")
                st.markdown(f"- Source: {r['source']}")
                st.markdown("---")
        else:
            st.warning("No reviews found or processed.")

if __name__ == "__main__":
    main()
