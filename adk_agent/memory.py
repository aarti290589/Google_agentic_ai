# memory.py
# (Optional, for hackathon template compliance)
# This module would log or store memory for the agent.
# In this project, memory is handled by BigQuery logging.

def log_memory(run_id, data):
    # Example: log to a file or database
    with open(f"memory_{run_id}.json", "w") as f:
        import json
        json.dump(data, f)

def retrieve_memory(run_id):
    # Example: retrieve from file
    try:
        with open(f"memory_{run_id}.json", "r") as f:
            import json
            return json.load(f)
    except FileNotFoundError:
        return None
