#!/bin/zsh
# Run both the Streamlit UI and dashboard in parallel
streamlit run ui_app.py &
sleep 2
streamlit run dashboard.py &
