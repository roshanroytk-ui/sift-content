import requests
import json
from datetime import datetime

import os
API_KEY = os.environ["GNEWS_API_KEY"]
URL = f"https://gnews.io/api/v4/top-headlines?lang=en&max=10&token={API_KEY}"

response = requests.get(URL)
data = response.json()

articles = []

for item in data.get("articles", []):
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
                "text": "Most people believe banks lend out money that already exists.They imagine banks as vaults — taking deposits from savers and handing that same money to borrowers."
            },
            {
                "type": "paragraph",
                "text": "That intuition feels natural. It’s also wrong."
            },
            {
                "type": "heading",
                "text": "The surprising truth"
            },
            {
                "type": "paragraph",
                "text": "In modern economies, most money is created when banks issue loans.When a bank approves your loan, it does not transfer existing money from someone else’s account."
            },
            {
                "type": "paragraph",
                "text": "Instead, it creates new money digitally by crediting your account with a deposit. Money appears — not from printing presses, but from accounting entries."
            },
            {
                "type": "heading",
                "text": "Why this matters"
            },
            {
                "type": "paragraph",
                "text": "Because money is created through lending, economies are highly sensitive to interest rates and financial confidence."
            },
            {
                "type": "heading",
                "text": "The takeaway"
            },
            {
                "type": "paragraph",
                "text": "Money is not a fixed pool. It expands and contracts based on trust, rules, and incentives."
            }
        ]
    },
    "news": articles
}

with open("daily_content.json", "w", encoding="utf-8") as f:
    json.dump(content, f, indent=2)

print("Content updated")
