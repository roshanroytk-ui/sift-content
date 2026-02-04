import requests
import json
from datetime import datetime

API_KEY = "REPLACED_BY_SECRET"
URL = f"https://gnews.io/api/v4/top-headlines?lang=en&max=10&token={API_KEY}"

response = requests.get(URL)
data = response.json()

articles = []

for item in data.get("articles", []):
    text = (item.get("title", "") + item.get("description", "")).lower()

    blocked = [
        "crime", "murder", "killed", "violence", "attack", "terror",
        "celebrity", "movie", "film", "sports", "match", "gossip"
    ]

    if any(word in text for word in blocked):
        continue

    articles.append({
        "title": item.get("title", ""),
        "description": item.get("description", ""),
        "source": item.get("source", {}).get("name", ""),
        "url": item.get("url", ""),
        "category": "General",
        "readingTime": 2
    })

content = {
    "updatedAt": datetime.utcnow().isoformat(),
    "insight": {
        "title": "How money is created out of thin air",
        "subtitle": "Why banks can create money when they lend",
        "readingTime": 5,
        "sections": [
            {
                "type": "paragraph",
                "text": "Most people believe banks lend out money that already exists."
            },
            {
                "type": "heading",
                "text": "The surprising truth"
            },
            {
                "type": "paragraph",
                "text": "In modern economies, most money is created when banks issue loans."
            },
            {
                "type": "paragraph",
                "text": "When a bank approves a loan, it creates new money digitally."
            },
            {
                "type": "heading",
                "text": "Why this matters"
            },
            {
                "type": "paragraph",
                "text": "This explains why interest rates affect inflation and growth."
            }
        ]
    },
    "news": articles[:5]
}

with open("daily_content.json", "w", encoding="utf-8") as f:
    json.dump(content, f, indent=2)

print("Content updated")
