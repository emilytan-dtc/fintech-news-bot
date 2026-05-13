import os
import time
import feedparser
import requests

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8902247453:AAEqh9rCScyjZfeFE6voBxWDcXjJdQU8u0A')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '1439804619')

FEEDS = [
    "https://cointelegraph.com/rss",
    "https://coindesk.com/arc/outboundfeeds/rss/",
    "https://www.theblockcrypto.com/rss.xml",
    "https://decrypt.co/feed",
    "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml",
]

seen = set()

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})

def check_feeds():
    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:
            if entry.link not in seen:
                seen.add(entry.link)
                msg = f"📰 <b>{entry.title}</b>\n{entry.link}"
                send_message(msg)
                time.sleep(1)

print("Bot started! Monitoring fintech & crypto news...")
send_message("🚀 Fintech News Bot is now live! You'll receive real-time alerts.")

while True:
    check_feeds()
    time.sleep(300)
