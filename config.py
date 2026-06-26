import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PROXY_URL = os.getenv("PROXY_URL")

# Google Vision
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Price tracking
PRICE_CHECK_HOUR = int(os.getenv("PRICE_CHECK_HOUR", "9"))
PRICE_DROP_THRESHOLD = float(os.getenv("PRICE_DROP_THRESHOLD", "5"))

# Scraping delays (seconds)
REQUEST_DELAY = 0.5

# Database
DATABASE_PATH = "price_tracker.db"

# Store URLs
WILDBERRIES_SEARCH_URL = "https://www.wildberries.ru/catalog/0/search.aspx?search={query}"
OZON_SEARCH_URL = "https://www.ozon.ru/search/?text={query}&from_global=true"
YANDEX_MARKET_SEARCH_URL = "https://market.yandex.ru/search?text={query}"