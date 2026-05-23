from flask import Flask
import requests
import time
import os
import threading
import xml.etree.ElementTree as ET

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

sent_links = set()

@app.route("/")
def home():
    return "ONDS bot is running ✅"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

def check_news():
    global sent_links

    rss_url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=ONDS&region=US&lang=en-US"

    while True:
        try:
            r = requests.get(rss_url)

            if r.status_code == 200:
                root = ET.fromstring(r.content)

                for item in root.findall(".//item")[:5]:
                    title = item.find("title").text
                    link = item.find("link").text

                    if link not in sent_links:
                        send(f"ONDS NEWS 🚨\n\n{title}\n{link}")
                        sent_links.add(link)

        except Exception as e:
            print(e)

        time.sleep(300)

threading.Thread(target=check_news, daemon=True).start()

port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
