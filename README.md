# Customer Feedback Analyzer

An AI-powered tool that reads through customer reviews, scores their sentiment, sorts them into business categories and writes an executive summary  all in seconds and mostly for free.

Built as part of my AI Engineering learning journey, extending the Cheezi Weezy Fast Food Assistant I built in Last previous project with a tool that helps a business actually understand its customers.

## The Problem

Small businesses collect customer feedback everywhere like Google reviews, Facebook comments, delivery app ratings  but rarely have time to read through it all, let alone spot patterns like "customers keep complaining about delivery speed" before it becomes a real problem.

This tool takes a pile of raw reviews and turns them into something a busy owner can act on in under a minute.

## What It Does

- **Analyzes sentiment** — instantly scores each review as positive or negative, with a confidence percentage
- **Categorizes automatically** — sorts every review into a business relevant bucket (Food Quality, Service, Delivery, Price, Cleanliness) with no manual tagging
- **Generates an executive summary** — a short, readable report covering overall sentiment, strongest areas, areas needing attention,and concrete next steps
- **Works out of the box** — includes 12 realistic sample reviews so you can see it working immediately

## How It Works

The project splits the work between two different kinds of AI, each doing the job it's actually good at:

1. **Local, open-source models** (Hugging Face pipelines) handle sentiment scoring and category classification — running entirely on your own machine, for free, with no API cost per review.
2. **A frontier LLM** (Google Gemini, or a local model via Ollama) reads the analyzed results and writes the final human readable summary, the kind of nuanced writing task frontier models are best at.

This mirrors how real production AI systems are often built: cheap, fast, local models for high volume repetitive work and a stronger model reserved for the part that actually needs it.

## Tech Stack

- **Python**
- **Hugging Face `transformers`** — sentiment analysis & zero-shot classification pipelines
- **PyTorch** — CPU-only inference backend
- **Google Gemini API** (via OpenAI compatible endpoint) —> summary generation
- **Ollama** (optional) — fully local, free alternative for summary generation
- **Gradio** — web interface
- **SQLite** — stores analyzed reviews

## Project Structure

customer-feedback-analyzer/
├── app.py # Gradio UI - run this to start the app
├── config.py # All settings: business name, categories, AI provider
├── database.py # SQLite storage for analyzed reviews
├── sentiment_pipeline.py # Hugging Face pipelines: sentiment + category
├── ai_client.py # Gemini / Ollama connection switcher
├── summary_generator.py # Builds the prompt & generates the summary
├── seed_data.py # Sample reviews to populate the demo
├── requirements.txt
├── .gitignore
└── .env # Your API key (not committed to git)



## Getting Started

### Prerequisites

- Python 3.10 or newer
- A free Google Gemini API key
- *(Optional)* [Ollama](https://ollama.com) installed, if you'd rather run the summary step fully locally instead of using Gemini

No Hugging Face account or token is needed — the models this project uses are public and freely downloadable.

### Installation

```bash
git clone https://github.com/ammar-ai-engineer/customer-feedback-analyzer.git
cd customer-feedback-analyzer

python -m venv venv
.\venv\Scripts\Activate.ps1      # Windows PowerShell
# source venv/bin/activate       # Mac/Linux

python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
```

> **Note:** `torch` is installed separately using PyTorch's CPU-only index, to avoid downloading several unnecessary gigabytes of GPU support on machines without a dedicated GPU. Using `python -m pip install` (rather than plain `pip install`) also avoids a known Windows security block on freshly created virtual environments.

### Environment Setup

Create a file named `.env` in the project root:

GOOGLE_API_KEY=your_gemini_api_key_here


### Running the App

```bash
python app.py
```

The first run automatically downloads two AI models (a few hundred MB total) — this only happens once. Every run after that is instant.

Once it's running, your terminal prints a local link like `http://127.0.0.1:7860` — open that in your browser.

## Switching Between Gemini and Ollama

Open `config.py` and change one line:

```python
AI_PROVIDER = "gemini"   # or "ollama"
```

To use Ollama, make sure it's running locally first (`ollama serve`), and that you've pulled a model matching `OLLAMA_MODEL` in `config.py` (e.g. `ollama pull llama3.2`).

## Customizing for Your Own Business

Everything you're likely to want to change lives in `config.py`:

- `BUSINESS_NAME` — shown in the app title
- `CATEGORIES` — the buckets reviews get sorted into; adjust these for any type of business

Want different sample data? Edit the `SAMPLE_REVIEWS` list in `seed_data.py`.

## Troubleshooting

**`ModuleNotFoundError` when running the app**
Your virtual environment probably isn't active. Look for `(venv)` at the start of your terminal prompt — if it's missing, run `.\venv\Scripts\Activate.ps1` and reinstall.

**Windows: "An Application Control policy has blocked this file"**
This is Windows Smart App Control blocking a freshly created `pip.exe`. Use `python -m pip install ...` instead of `pip install ...` directly — this routes the install through your already-trusted Python interpreter instead.

**First run feels slow or stuck**
Normal — the sentiment and classification models are downloading for the first time. Later runs are instant, since both are cached locally afterward.

## Possible Future Improvements

- Bulk-upload reviews from a CSV file instead of typing them one at a time
- Sentiment trend charts over time
- Multi-language review support
- Direct integration with a real review source (Google Business, Facebook)



