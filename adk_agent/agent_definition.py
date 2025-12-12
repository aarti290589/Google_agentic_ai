# adk_agent/agent_definition.py

from adk_agent.tools.data_ingestion import fetch_reviews, call_gemini_api
from adk_agent.schemas.output_models import ReviewAnalysisResult
from data_processing.data_writer import write_to_bigquery, list_bigquery_tables
from concurrent.futures import ThreadPoolExecutor, as_completed

def analyze_review_with_gemini(review, config):
    text = review.get('text', '') or review.get('review_text', '')
    # Use rating to determine sentiment
    rating = review.get('rating', None)
    if rating is not None:
        try:
            rating = float(rating)
            sentiment = 'Good' if rating >= 4 else 'Bad'
        except Exception:
            sentiment = 'Unknown'
    else:
        sentiment = 'Unknown'
    # Short, efficient prompt for aspect and recommendations only
    prompt = f"""
Analyze this restaurant review: \"{text}\"\nReturn JSON: aspect (main topic), recommendation (3 short actions).
"""
    response = call_gemini_api(prompt, project_id=getattr(config, 'VERTEX_AI_PROJECT_ID', None))
    import json
    try:
        cleaned = response.strip().removeprefix('```json').removesuffix('```').strip()
        result = json.loads(cleaned)
        # If result is a list, use the first element
        if isinstance(result, list) and len(result) > 0:
            aspect = result[0].get('aspect', '')
            recommendation = result[0].get('recommendation', [])
        elif isinstance(result, dict):
            aspect = result.get('aspect', '')
            recommendation = result.get('recommendation', [])
        else:
            aspect = ''
            recommendation = []
        # Ensure aspect is a string, not a list
        if isinstance(aspect, list):
            aspect = aspect[0] if aspect else ''
        return ReviewAnalysisResult(
            review_text=text,
            sentiment=sentiment,
            aspect=aspect,
            recommendation=recommendation
        )
    except Exception as e:
        print(f"[GEMINI ERROR] {e}. Raw response: {response}")
        return ReviewAnalysisResult(
            review_text=text,
            sentiment=sentiment,
            aspect='Unknown',
            recommendation=[]
        )

def run_agent_pipeline(config):
    print("[AGENT] Running agent pipeline with Gemini...")
    place_name = getattr(config, 'PLACE_NAME', None)
    location = getattr(config, 'LOCATION', None)
    if not place_name or not location:
        raise ValueError("PLACE_NAME and LOCATION must be set in your configuration or .env file.")
    all_results = []
    reviews = fetch_reviews(place_name, source='google', location=location)
    # Limit to first 5 reviews for faster testing
    reviews = reviews[:5]
    # Parallelize Gemini API calls with higher parallelism
    results = []
    with ThreadPoolExecutor(max_workers=20) as executor:  # Increased from 5 to 20
        future_to_review = {executor.submit(analyze_review_with_gemini, review, config): review for review in reviews}
        for future in as_completed(future_to_review):
            analysis = future.result()
            results.append({
                'review_text': analysis.review_text,
                'sentiment': analysis.sentiment,
                'aspect': analysis.aspect,
                'recommendation': analysis.recommendation,
                'source': 'google',
                'restaurant_name': place_name,
                'location': location
            })
    # List tables for debugging
    list_bigquery_tables()
    if results:
        write_to_bigquery(results)
    else:
        print("[AGENT] No reviews found. Skipping BigQuery write.")
    return results
