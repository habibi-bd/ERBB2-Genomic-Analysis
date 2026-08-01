import time
import random
import sqlite3
from curl_cffi import requests
from bs4 import BeautifulSoup

DB_NAME = "/mnt/d/PriceTracker/linux/price_tracker.db"


def get_tracked_asins():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT asin FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]


def parse_direct_price(html):
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")

    # Target common Amazon product page price structures
    price_el = (
        soup.select_one("span.a-price span.a-offscreen")
        or soup.select_one("#priceblock_ourprice")
        or soup.select_one("#priceblock_dealprice")
    )
    if price_el:
        try:
            price_str = price_el.get_text(strip=True).replace("$", "").replace(",", "")
            return float(price_str)
        except:
            return None
    return None


def log_price(asin, price):
    if price is None:
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO price_history (asin, price, timestamp)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    """,
        (asin, price),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    asins = get_tracked_asins()
    if not asins:
        print("⚠️ No ASINs found in the system database. Run 'discovery.py' first!")
        exit()

    session = requests.Session(impersonate="chrome")
    print(f"📈 Extracting Real-Time Prices for {len(asins)} Target ASINs...")

    for idx, asin in enumerate(asins, 1):
        url = f"https://www.amazon.com/dp/{asin}"
        print(f"[{idx}/{len(asins)}] Streaming price for ASIN: {asin}")

        try:
            res = session.get(url, timeout=15)
            if res.status_code == 200:
                price = parse_direct_price(res.text)
                if price:
                    log_price(asin, price)
                    print(f"   💰 Live Price Logged: ${price}")
                else:
                    print("   ⚠️ Price element not found or block encountered.")
            else:
                print(f"   ❌ HTTP Error status code: {res.status_code}")
        except Exception as e:
            print(f"   ❌ Connection failed: {e}")

        # Pacing to protect connection session
        time.sleep(random.uniform(5.0, 9.0))
