from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import praw, os, logging

load_dotenv()

if not all([os.getenv("REDDIT_CLIENT_ID"), os.getenv("REDDIT_CLIENT_SECRET"), os.getenv("REDDIT_USER_AGENT")]):
    raise RuntimeError("Missing Reddit API credentials. Check your .env file.")

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)
app = FastAPI()
analyzer = SentimentIntensityAnalyzer()

logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class InputData(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

def get_sentiment(text: str):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return label, round(abs(compound), 3)

def fetch_reddit_text(url: str):
    submission = reddit.submission(url=url)
    return (submission.title or "") + "\n" + (submission.selftext or "")

@app.post("/analyze")
async def analyze(inputs: List[InputData]):
    results = []
    for item in inputs:
        if not item.text and not item.url:
            results.append({"error": "Provide either text or url"})
            continue

        if item.text:
            label, confidence = get_sentiment(item.text)
            results.append({
                "source": "raw",
                "text": item.text,
                "label": label,
                "confidence": confidence,
                "model": "VADER"
            })

        if item.url:
            try:
                reddit_text = fetch_reddit_text(item.url)
                label, confidence = get_sentiment(reddit_text)
                results.append({
                    "source": "reddit",
                    "url": item.url,
                    "text": reddit_text,
                    "label": label,
                    "confidence": confidence,
                    "model": "VADER"
                })
            except Exception as e:
                results.append({"error": f"Failed to fetch Reddit content: {str(e)}"})

    return {"results": results}
