# reporting/notification_service.py

def send_report(results):
    print("[REPORTING] Sending report...")
    if not results:
        print("[REPORTING] No results to report.")
        return
    # Example: Print summary to console (replace with email/Looker integration as needed)
    negative = [r for r in results if r['sentiment'] == 'Negative']
    print(f"[REPORTING] Total reviews analyzed: {len(results)}")
    print(f"[REPORTING] Negative reviews: {len(negative)}")
    if negative:
        print("[REPORTING] Sample negative review and recommendations:")
        print(f"Text: {negative[0]['review_text']}")
        print(f"Aspect: {negative[0]['aspect']}")
        print(f"Recommendations: {negative[0]['recommendation']}")
