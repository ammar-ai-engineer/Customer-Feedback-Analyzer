# The Gradio UI - ties every other file together into one working app.


import gradio as gr
from database import init_db, get_all_reviews, add_review
from sentiment_pipeline import analyze_review
from summary_generator import generate_summary
from seed_data import seed_database
from config import BUSINESS_NAME

# Make sure the database and table exist before the app even opens
init_db()


def analyze_new_review(review_text):
    """
    Called when the user submits one new review through the UI.
    Analyzes it, saves it, and returns the refreshed reviews table.
    """
    if not review_text.strip():
        return get_reviews_table(), ""

    analysis = analyze_review(review_text)
    add_review(
        review_text=review_text,
        category=analysis["category"],
        sentiment_label=analysis["sentiment_label"],
        sentiment_score=analysis["sentiment_score"],
    )
    return get_reviews_table(), ""  # refresh table, clear the textbox


def get_reviews_table():
    """
    Fetches all reviews and reshapes them into rows Gradio's
    Dataframe component can display.
    """
    reviews = get_all_reviews()
    rows = [
        [r["review_text"], r["category"], r["sentiment_label"], f"{r['sentiment_score']*100:.1f}%"]
        for r in reviews
    ]
    return rows


def run_summary():
    """
    Called when the user clicks 'Generate Summary'.
    """
    reviews = get_all_reviews()
    return generate_summary(reviews)


def load_sample_data():
    """
    Called when the user clicks 'Load Sample Reviews'.
    """
    seed_database()
    return get_reviews_table()


with gr.Blocks(title=f"{BUSINESS_NAME} - Feedback Analyzer") as demo:
    gr.Markdown(f"# {BUSINESS_NAME} - Customer Feedback Analyzer")
    gr.Markdown("Paste a customer review below, or load sample data to see it in action.")

    with gr.Row():
        review_input = gr.Textbox(label="New Review", placeholder="Type or paste a customer review here...", lines=2)
        submit_btn = gr.Button("Analyze & Save")

    reviews_table = gr.Dataframe(
        headers=["Review", "Category", "Sentiment", "Confidence"],
        label="All Reviews",
        value=get_reviews_table(),
    )

    with gr.Row():
        sample_btn = gr.Button("Load Sample Reviews")
        summary_btn = gr.Button("Generate Summary", variant="primary")

    summary_output = gr.Markdown(label="Business Summary")

    submit_btn.click(analyze_new_review, inputs=review_input, outputs=[reviews_table, review_input])
    sample_btn.click(load_sample_data, outputs=reviews_table)
    summary_btn.click(run_summary, outputs=summary_output)


if __name__ == "__main__":
    demo.launch()