import time
import random
import sqlite3
from curl_cffi import requests
from bs4 import BeautifulSoup

DB_NAME = "/mnt/d/PriceTracker/linux/price_tracker.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Table to hold unique products discovered
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            asin TEXT PRIMARY KEY,
            title TEXT,
            rating REAL,
            review_count INTEGER,
            last_discovered TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Table to stream historical price records
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asin TEXT,
            price REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (asin) REFERENCES products (asin)
        )
    """)
    conn.commit()
    conn.close()


def parse_search_results(html):
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")

    # Target all possible container classes Amazon rotates through
    products = (
        soup.select("div[data-asin]")
        or soup.select(".s-result-item")
        or soup.select("[data-component-type='s-search-result']")
    )

    discovered = []
    for product in products:
        # Fallback tracking if data-asin attribute is embedded differently
        asin = product.get("data-asin") or product.get("data-item-id")
        if not asin or len(asin.strip()) == 0 or asin == "None":
            continue

        # Target resilient structural variations for headers
        title_el = (
            product.select_one("h2 a span")
            or product.select_one("h2 span")
            or product.select_one(".a-size-medium")
            or product.select_one(".a-size-base-plus")
        )
        title = title_el.get_text(strip=True) if title_el else "N/A"
        if title == "N/A":
            continue

        rating_el = product.select_one(
            "i.a-icon-star span, i.a-icon-star-small span, .a-icon-alt"
        )
        rating = None
        if rating_el:
            try:
                rating = float(rating_el.get_text(strip=True).split()[0])
            except:
                pass

        review_count_el = product.select_one(
            "span.a-size-base[dir='auto'], a.s-underline-text span"
        )
        review_count = 0
        if review_count_el:
            try:
                review_count = int(
                    review_count_el.get_text(strip=True)
                    .replace("(", "")
                    .replace(")", "")
                    .replace(",", "")
                )
            except:
                pass

        discovered.append((asin, title, rating, review_count))

    return discovered


def save_discovered_products(products_list):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    for item in products_list:
        cursor.execute(
            """
            INSERT INTO products (asin, title, rating, review_count, last_discovered)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(asin) DO UPDATE SET
                rating=excluded.rating,
                review_count=excluded.review_count,
                last_discovered=CURRENT_TIMESTAMP
        """,
            item,
        )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    search_keywords = ["smartwatch", "fitness tracker watch"]
    session = requests.Session(impersonate="chrome")

    print("🚀 Running Discovery Pipeline...")
    for kw in search_keywords:
        url_keyword = kw.replace(" ", "+")
        url = f"https://www.amazon.com/s?k={url_keyword}&page=1"
        try:
            res = session.get(url, timeout=15)
            if res.status_code == 200:
                items = parse_search_results(res.text)
                save_discovered_products(items)
                print(f"✅ Discovered & Updated {len(items)} items for keyword: '{kw}'")
        except Exception as e:
            print(f"❌ Error exploring '{kw}': {e}")
        time.sleep(random.uniform(4.0, 7.0))
