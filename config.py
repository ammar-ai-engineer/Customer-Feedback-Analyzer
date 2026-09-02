
# All the settings for our Customer Feedback Analyzer, in one place.
# Change something here, and it affects the whole project - no hunting
# through other files.

# Business Info 
BUSINESS_NAME = "Cheezi Weezy Fast Food"

# Review Categories
# Every review will get sorted into one of these buckets.
# Change these if you want to use this for a different kind of business.
CATEGORIES = [
    "Food Quality",
    "Service",
    "Delivery",
    "Price",
    "Cleanliness",
]

#  AI Provider Settings
# "gemini" = your paid key, better quality, needs internet
# "ollama" = free, runs on your own machine, needs Ollama running locally
AI_PROVIDER = "gemini"

GEMINI_MODEL = "gemini-2.5-flash"
OLLAMA_MODEL = "llama3.2"

# Database
DB_PATH = "feedback.db"

# Summary Prompt
SUMMARY_SYSTEM_PROMPT = """
You are a business analyst who reads customer feedback data and writes
clear, actionable summaries for a business owner. Highlight what's going
well, what needs attention, and suggest 2-3 concrete next steps.
Write in markdown, without code blocks.
"""