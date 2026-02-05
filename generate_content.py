import requests
import json
from datetime import datetime

import os
API_KEY = os.environ["GNEWS_API_KEY"]
GEMINI_KEY = os.environ["GEMINI_API_KEY"]

# ✅ Multiple countries to bypass 10-article limit per request
urls = [
    f"https://gnews.io/api/v4/top-headlines?country=us&lang=en&token={API_KEY}",
    f"https://gnews.io/api/v4/top-headlines?country=in&lang=en&token={API_KEY}",
    f"https://gnews.io/api/v4/top-headlines?country=gb&lang=en&token={API_KEY}",
    f"https://gnews.io/api/v4/search?q=technology&lang=en&token={API_KEY}",
    f"https://gnews.io/api/v4/search?q=business&lang=en&token={API_KEY}",
    f"https://gnews.io/api/v4/search?q=innovation&lang=en&token={API_KEY}",
    f"https://gnews.io/api/v4/search?q=business&lang=en&token={API_KEY}",
]

articles = []

for u in urls:
    response = requests.get(u).json()

    for item in response.get("articles", []):
        articles.append({
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "source": item.get("source", {}).get("name", ""),
            "url": item.get("url", ""),
            "category": "General",
            "readingTime": 2
        })

# ✅ remove duplicates (same story across countries)
seen = set()
unique_articles = []

for a in articles:
    if a["url"] not in seen:
        seen.add(a["url"])
        unique_articles.append(a)

articles = unique_articles

def generate_insight():
    prompt = """
    Write a calm, thoughtful daily insight (300–400 words).

    Tone: intelligent, optimistic, reflective
    Topics: economics, technology, society, learning, long-term thinking
    Avoid: crime, fear, gossip, celebrity news

    Structure:
    - Short engaging opening
    - Clear explanation
    - Gentle takeaway

    Return plain paragraphs only (no markdown).
    """

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_KEY}",
        json={
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }
    ).json()

    text = response["candidates"][0]["content"]["parts"][0]["text"]

    return {
        "title": "Daily Insight",
        "subtitle": "A calm perspective",
        "readingTime": 3,
        "sections": [
            {"type": "paragraph", "text": p}
            for p in text.split("\n\n") if p.strip()
        ]
    }

    r = requests.post(url, json=payload)
    response = r.json()

    if "candidates" not in response:
        print("Gemini error:", response)
        return {
            "title": "Daily Insight",
            "subtitle": "AI temporarily unavailable",
            "readingTime": 1,
            "sections": [
                {"type": "paragraph", "text": "Insight will refresh tomorrow."}
            ]
        }

    text = response["candidates"][0]["content"]["parts"][0]["text"]

    return {
        "title": "Daily Insight",
        "subtitle": "A calm perspective",
        "readingTime": 3,
        "sections": [
            {"type": "paragraph", "text": p.strip()}
            for p in text.split("\n\n")
            if p.strip()
        ]
    }


content = {
    "updatedAt": datetime.utcnow().isoformat(),
    "insight": generate_insight(),
    "news": articles
}

with open("daily_content.json", "w", encoding="utf-8") as f:
    json.dump(content, f, indent=2)

print("Content updated")
