from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_gold_price():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
    })

    # سعر الذهب العالمي
    gold_url = "https://data-asg.goldprice.org/dbXRates/USD"
    gold_response = session.get(gold_url, timeout=3)
    gold_data = gold_response.json()
    gold_price_usd = gold_data["items"][0]["xauPrice"]

    # سعر الدولار مقابل الجنيه
    alsoug_url = "https://www.alsoug.com/currency"
    alsoug_response = session.get(alsoug_url, timeout=5)
    soup = BeautifulSoup(alsoug_response.text, "lxml")
    usd_input = soup.find("input", id="usd-sdg-alternate")
    usd_to_sdg = int(usd_input["value"])

    # الحساب
    gold_price = round((((gold_price_usd / 31.1) * 0.875) * usd_to_sdg))
    return gold_price


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/price")
def price():
    return jsonify({
        "gold_price": get_gold_price()  # رقم فقط
    })


if __name__ == "__main__":
    app.run(debug=True)
