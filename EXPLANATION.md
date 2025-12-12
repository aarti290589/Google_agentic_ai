# EXPLANATION.md

## Agent Reasoning Process
- Receives user input (restaurant, location) via Streamlit UI.
- Fetches reviews from Google Places API.
- For each review:
  - Uses the rating to set sentiment: below 4 stars = 'Bad', 4 or above = 'Good'.
  - Calls Gemini API to extract aspect and recommendations.
- Results are written to BigQuery with restaurant/location for filtering.
- Dashboard visualizes only the current restaurant/location's results.

## Memory Usage
- No persistent memory module, but all results are logged in BigQuery (can be used as memory/log).
- Each run is filterable by restaurant/location.

## Planning Style
- Simple sequential pipeline (could be extended to ReAct/BabyAGI).
- No explicit planner/executor modules, but logic is modular and could be refactored.

## Tool Integration
- **Gemini API**: Used for aspect/recommendation extraction.
- **Google Places API**: For review ingestion.
- **BigQuery**: For storage and dashboard queries.

## Known Limitations
- No advanced memory or multi-step planning (all logic is sequential).
- No error recovery if Gemini or Google APIs fail.
- No user authentication or access control.
- Table schema changes require manual intervention.
- Only supports English reviews.

---

## How to Extend
- Add a `memory.py` to log/retrieve past runs.
- Refactor agent logic into `planner.py` and `executor.py` for more complex planning.
- Add more tool integrations (Yelp, synthetic data, etc.).
- Add user authentication for multi-user support.
