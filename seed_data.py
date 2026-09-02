# Fills the database with sample customer reviews, so the demo works
# right away. This is also the first file that connects
# sentiment_pipeline.py and database.py together.

from database import init_db, clear_all_reviews, add_review
from sentiment_pipeline import analyze_review

SAMPLE_REVIEWS = [
    "The zinger burger was amazing, best I've had in town!",
    "Waited over an hour for delivery and the food was cold when it arrived.",
    "Staff was really friendly and helped me pick a combo deal.",
    "Way too expensive for the portion size you get.",
    "The restaurant floor was sticky and the tables weren't cleaned properly.",
    "Fries were fresh and hot, exactly how I like them.",
    "Rider was rude on the phone when I asked about my order status.",
    "Great value for money, the family deal fed all of us easily.",
    "Order was completely wrong, I asked for no onions and it was full of them.",
    "Loved the ambiance, very clean and family friendly.",
    "Delivery was actually faster than expected, food still hot.",
    "Prices went up but the quality feels the same as before.",
]


def seed_database():
    """
    Wipes any existing reviews, then analyzes and stores each sample
    review fresh. Run this once to populate the demo with data.
    """
    init_db()
    clear_all_reviews()

    for review_text in SAMPLE_REVIEWS:
        analysis = analyze_review(review_text)
        add_review(
            review_text=review_text,
            category=analysis["category"],
            sentiment_label=analysis["sentiment_label"],
            sentiment_score=analysis["sentiment_score"],
        )
        print(f"Added [{analysis['category']} | {analysis['sentiment_label']}]: {review_text[:40]}...")

    print(f"\nSeeded {len(SAMPLE_REVIEWS)} reviews successfully!")


if __name__ == "__main__":
    seed_database()