"""
main_workflow.py
Entry point for the Agentic AI review analysis pipeline.
Handles configuration, agent orchestration, and reporting trigger.
"""

import os
import json
import webbrowser
import subprocess
from config.settings import settings
from adk_agent.agent_definition import run_agent_pipeline
from reporting.notification_service import send_report

# 1. Read configuration (API keys, project settings, etc.)
def load_config():
    # Use settings object from config/settings.py
    return settings

# 2. Call the Agent to run the analysis pipeline
def run_agentic_analysis(config):
    print("[INFO] Running agentic analysis pipeline...")
    # Run the agent pipeline and get results
    results = run_agent_pipeline(config)
    return results

# 3. Trigger reporting/dashboard update
def trigger_reporting(config, results=None):
    print("[INFO] Triggering reporting/dashboard update...")
    # Send report/notification with results
    send_report(results)

def launch_dashboard():
    # Start the Streamlit dashboard in the background
    subprocess.Popen(["streamlit", "run", "dashboard.py"])
    # Open the dashboard in the default browser
    webbrowser.open("http://localhost:8501")

def main():
    config = load_config()
    results = run_agentic_analysis(config)
    trigger_reporting(config, results)
    launch_dashboard()  # Launch dashboard after analysis

if __name__ == "__main__":
    main()
