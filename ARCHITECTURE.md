# ARCHITECTURE.md

## System Architecture Overview

```
+-------------------+      +-------------------+      +-------------------+
|   Streamlit UI    | ---> |   Agent Workflow  | ---> |   BigQuery Table  |
| (src/ui_app.py,   |      | (src/adk_agent/   |      | (review_analysis) |
|  src/unified_app) |      |  agent_definition)|      +-------------------+
+-------------------+      +-------------------+      |  Stores analyzed  |
| User input:       |      | 1. Receives input |      |  reviews, aspects |
| - Restaurant      |      | 2. Plans (simple) |      |  sentiment, recs  |
| - Location        |      | 3. Calls Gemini   |      +-------------------+
|                   |      | 4. Writes to BQ   |
+-------------------+      +-------------------+
```

### Core Modules
- **planner.py**: (to be created) - would break down user goals into sub-tasks (currently logic is in agent_definition.py)
- **executor.py**: (to be created) - would handle LLM/tool calls (currently logic is in agent_definition.py)
- **memory.py**: (to be created) - would log/store memory (currently not used, but could log to BigQuery or local file)

### Tool Integrations
- **Gemini API**: Used for review analysis (aspect/recommendation extraction)
- **Google Places API**: For review ingestion
- **BigQuery**: For storing and retrieving analysis results

### Logging & Observability
- Print/debug statements in all major modules
- Error handling for API and BigQuery calls

### Data Flow
1. User enters restaurant/location in UI
2. Reviews are fetched from Google Places
3. Each review is analyzed by Gemini (sentiment, aspect, recommendations)
4. Results are written to BigQuery
5. Dashboard visualizes results from BigQuery

---

## Diagram (ASCII)

```
[User] -> [Streamlit UI] -> [Agentic Pipeline] -> [Gemini API]
                                         |                |
                                         v                v
                                 [BigQuery Table] <- [Google Places API]
                                         |
                                         v
                                 [Streamlit Dashboard]
```

---

## Notes
- All code is under `src/` (or `adk_agent/`, `data_processing/`, etc. in this repo)
- Gemini API key is stored in `.env` (not committed)
- No explicit memory module, but BigQuery can serve as memory/log
- Planning is simple (sequential), but could be extended to ReAct/BabyAGI style
