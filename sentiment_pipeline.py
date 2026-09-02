# This does the real "thinking" - the exact pipeline() pattern


from transformers import pipeline
from config import CATEGORIES

# Build both pipelines ONCE, when this file first loads.
# Same "build once, call many times"
# without a GPU, so we just let it use the CPU.
sentiment_analyzer = pipeline("sentiment-analysis")
category_classifier = pipeline("zero-shot-classification")


def analyze_review(review_text):
    """
    Takes one review's text.
    Returns its sentiment (positive/negative + confidence),
    and which category it best fits into.
    """
    # Step 1: sentiment
    sentiment_result = sentiment_analyzer(review_text)[0]
    sentiment_label = sentiment_result["label"]
    sentiment_score = sentiment_result["score"]

    # Step 2: category
    category_result = category_classifier(review_text, candidate_labels=CATEGORIES)
    top_category = category_result["labels"][0]

    return {
        "sentiment_label": sentiment_label,
        "sentiment_score": sentiment_score,
        "category": top_category,
    }