from telethon import TelegramClient, events
import re
import os
from datetime import datetime

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient("bot", api_id, api_hash)

channels = [
    "financialjuice",
    "marketfeed"
]

bullish_words = [
    "rate cut",
    "dovish",
    "recession",
    "weak data",
    "cpi lower",
    "unemployment rise"
]

bearish_words = [
    "rate hike",
    "hawkish",
    "strong jobs",
    "cpi higher",
    "inflation rising",
    "economy strong"
]

high_impact = [
    "CPI",
    "NFP",
    "FOMC",
    "Powell",
    "Fed Chair",
    "Interest Rate",
    "Rate Decision"
]

def analyze_news(text):

    score = 0

    for word in bullish_words:
        if word.lower() in text.lower():
            score += 1

    for word in bearish_words:
        if word.lower() in text.lower():
            score -= 1

    if score > 0:
        signal = "BUY GOLD"
    elif score < 0:
        signal = "SELL GOLD"
    else:
        signal = "NEUTRAL"

    confidence = min(abs(score) * 25, 90)

    return signal, confidence


@client.on(events.NewMessage(chats=channels))
async def handler(event):

    text = event.raw_text

    signal, confidence = analyze_news(text)

    impact = "LOW"

    for word in high_impact:
        if word.lower() in text.lower():
            impact = "HIGH"

    if impact == "HIGH":

        print("")

        print("🚨 HIGH IMPACT NEWS DETECTED")
        print(text)

        print("")
        print("📊 SIGNAL :", signal)
        print("🎯 CONFIDENCE :", confidence,"%")
        print("⏰ TIME :", datetime.now())

        print("")


print("AI NEWS SNIPER GOLD BOT RUNNING...")

client.start()
client.run_until_disconnected()
