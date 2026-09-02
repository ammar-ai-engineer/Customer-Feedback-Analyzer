# Takes all the analyzed reviews, and asks the AI to write a
# real summary from them 

from ai_client import get_client_and_model
from config import SUMMARY_SYSTEM_PROMPT, BUSINESS_NAME


def build_reviews_text(reviews):
    """
    Turns the list of review dictionaries into one readable block of text,
    so the AI can read them like a report instead of raw database rows.
    """
    lines = []
    for review in reviews:
        line = f"- [{review['category']} | {review['sentiment_label']}] {review['review_text']}"
        lines.append(line)
    return "\n".join(lines)


def generate_summary(reviews):
    """
    Given all analyzed reviews, ask the AI to write an executive summary.
    """
    if not reviews:
        return "No reviews yet - add some feedback first!"

    reviews_text = build_reviews_text(reviews)

    user_prompt = f"""
Business: {BUSINESS_NAME}

Below are {len(reviews)} customer reviews, each already tagged with a
category and sentiment. Write a short executive summary covering:
- Overall sentiment trend
- Strongest category
- Category that needs the most attention
- 2-3 concrete action items

Reviews:
{reviews_text}
"""

    messages = [
        {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    client, model = get_client_and_model()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content