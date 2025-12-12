# executor.py
# (Optional, for hackathon template compliance)
# This module would handle LLM/tool calls for the agent.
# In this project, execution is handled in agent_definition.py.

def execute(task, context):
    # Example: call the right function for each task
    if task == "fetch_reviews":
        return context['fetch_reviews']()
    elif task == "analyze_reviews":
        return context['analyze_reviews']()
    elif task == "store_results":
        return context['store_results']()
    elif task == "report_results":
        return context['report_results']()
    else:
        raise ValueError(f"Unknown task: {task}")
