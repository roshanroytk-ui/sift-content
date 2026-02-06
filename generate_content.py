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
    Write an interesting fact or facinating explainer about how the world works, focused on economics, finance, business, technology, or science.

    FORMAT EXACTLY LIKE THIS:

    TITLE: <short curiosity title>
    SUBTITLE: <one-line calm subtitle>
    BODY:
    <paragraph 1>

    <paragraph 2>

    <paragraph 3>

    Tone: clear, engaging, explainer, no technical jargon
    Topics: economics, finance, business , science
    Avoid crime, fear, gossip, and celebrity news.
    """

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_KEY}",
        json={
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }
    ).json()

    if "candidates" not in response:
        print("Gemini error:", response)
        return {
            "title": "Daily Insight",
            "subtitle": "A calm perspective",
            "readingTime": 1,
            "sections": [
                {"type": "paragraph", "text": "Insight will refresh tomorrow."}
            ]
        }

    text = response["candidates"][0]["content"]["parts"][0]["text"]

    # ---- parse title & subtitle ----
    title = "Daily Insight"
    subtitle = "A calm perspective"

    for line in text.splitlines():
        if line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
        elif line.startswith("SUBTITLE:"):
            subtitle = line.replace("SUBTITLE:", "").strip()

    # ---- parse body ----
    body = text.split("BODY:", 1)[1] if "BODY:" in text else text

    sections = [
        {"type": "paragraph", "text": p.strip()}
        for p in body.split("\n\n") if p.strip()
    ]

    return {
        "title": title,
        "subtitle": subtitle,
        "readingTime": 3,
        "sections": sections
    }


content = {
    "updatedAt": datetime.utcnow().isoformat(),
    "insight": generate_insight(),
    "news": articles
}

with open("daily_content.json", "w", encoding="utf-8") as f:
    json.dump(content, f, indent=2)

print("Content updated")
