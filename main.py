import os
import time
import feedparser
import requests
from datetime import datetime, timezone, timedelta

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8902247453:AAEqh9rCScyjZfeFE6voBxWDcXjJdQU8u0A')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '1439804619')

FEEDS = [
    "https://cointelegraph.com/rss",
    "https://coindesk.com/arc/outboundfeeds/rss/",
    "https://www.theblockcrypto.com/rss.xml",
    "https://decrypt.co/feed",
]

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})

def check_feeds():
    cutoff = datetime.now(timezone.utc) - timedelta(hours=7)
    articles = []
    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:10]:
            try:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                if published > cutoff:
                    articles.append((published, entry.title, entry.link))
            except:
                pass
    articles.sort(reverse=True)
    if articles:
        send_message("📰 <b>Fintech & Crypto News Update</b>")
        for _, title, link in articles[:10]:
            send_message(f"• <b>{title}</b>\n{link}")
            time.sleep(1)
    else:
        send_message("📭 No new fintech news in the last 7 hours.")

check_feeds()
