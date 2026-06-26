# Price Bot Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent (recommended) or compose:execute to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add categories, price history charts, and sale notifications to the price comparison bot.

**Architecture:** Extend existing SQLite database with new tables for categories and price history. Add Telegram bot commands for category browsing and price tracking. Schedule daily price checks with notifications.

**Tech Stack:** Python 3.11+, python-telegram-bot, SQLite, aiosqlite, matplotlib (for charts)

## Global Constraints

- Python 3.11+ required
- All API keys stored in .env file, never committed
- Telegram bot token from @BotFather
- Price tracking checks once daily at configurable time
- MVP scope: Wildberries, Ozon, Яндекс.Маркет only
- All scrapers must handle rate limiting with delays
- No hardcoded URLs - use config.py for all endpoints

---

## File Structure

```
price-compare-bot/
├── bot.py              # Telegram bot entry point (MODIFY)
├── config.py           # Configuration and env loading (MODIFY)
├── database.py         # SQLite operations (MODIFY)
├── search.py           # Search orchestrator (MODIFY)
├── categories.py       # Category definitions (CREATE)
├── price_history.py    # Price history tracking (CREATE)
├── notifications.py    # Sale notifications (CREATE)
├── charts.py           # Price charts generation (CREATE)
├── scrapers/           # Store scrapers (NO CHANGE)
├── tests/              # Test files (MODIFY)
├── requirements.txt    # Dependencies (MODIFY)
└── README.md           # Documentation (MODIFY)
```

---

## Task 1: Category System

**Covers:** Categories feature

**Files:**
- Create: `price-compare-bot/categories.py`
- Modify: `price-compare-bot/bot.py`
- Create: `price-compare-bot/tests/test_categories.py`

**Interfaces:**
- Produces: `CATEGORIES` dict, `get_category_products(category)`, `search_by_category(query, category)`

- [ ] **Step 1: Write failing test**

```python
# tests/test_categories.py
import pytest
from categories import CATEGORIES, get_category_products, search_by_category

def test_categories_exist():
    assert len(CATEGORIES) > 0
    assert "shampoo" in CATEGORIES
    assert "cream" in CATEGORIES

def test_get_category_products():
    products = get_category_products("shampoo")
    assert isinstance(products, list)
    assert len(products) > 0

def test_search_by_category():
    results = search_by_category("Dove", "shampoo")
    assert isinstance(results, list)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_categories.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: Implement categories.py**

```python
# categories.py
CATEGORIES = {
    "shampoo": {
        "name": "Шампуни",
        "keywords": ["шампунь", "shampoo", "для волос"],
        "emoji": "🧴"
    },
    "cream": {
        "name": "Кремы",
        "keywords": ["крем", "cream", "уход за кожей"],
        "emoji": "🧴"
    },
    "gel": {
        "name": "Гели для душа",
        "keywords": ["гель для душа", "gel", "душ"],
        "emoji": "🚿"
    },
    "deodorant": {
        "name": "Дезодоранты",
        "keywords": ["дезодорант", "deodorant", "антиперспирант"],
        "emoji": "💨"
    },
    "perfume": {
        "name": "Парфюмерия",
        "keywords": ["парфюм", "perfume", "туалетная вода", "духи"],
        "emoji": "💐"
    },
    "makeup": {
        "name": "Макияж",
        "keywords": ["помада", "тушь", "подводка", "makeup"],
        "emoji": "💄"
    }
}

def get_category_products(category: str) -> List[Dict]:
    if category not in CATEGORIES:
        return []
    cat = CATEGORIES[category]
    return [{"name": cat["name"], "emoji": cat["emoji"], "keywords": cat["keywords"]}]

def search_by_category(query: str, category: str) -> List[Dict]:
    if category not in CATEGORIES:
        return []
    cat = CATEGORIES[category]
    extended_query = query + " " + " ".join(cat["keywords"][:2])
    return [{"query": extended_query, "category": category}]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_categories.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add price-compare-bot/categories.py price-compare-bot/tests/test_categories.py
git commit -m "feat: add category system"
```

---

## Task 2: Category Bot Commands

**Covers:** Categories feature

**Files:**
- Modify: `price-compare-bot/bot.py`
- Modify: `price-compare-bot/tests/test_bot.py`

**Interfaces:**
- Consumes: categories.py, search.py
- Produces: `/categories`, `/category <name>` commands

- [ ] **Step 1: Write failing test**

```python
# Add to tests/test_bot.py
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from bot import categories_command, category_command

@pytest.mark.asyncio
async def test_categories_command():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    
    await categories_command(update, context)
    
    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args[0][0]
    assert "Шампуни" in call_args
    assert "Кремы" in call_args

@pytest.mark.asyncio
@patch('search.search_all_stores')
async def test_category_command(mock_search):
    mock_search.return_value = [{"name": "Dove шампунь", "price": 189, "url": "test.ru", "store": "Ozon"}]
    update = MagicMock()
    update.message.text = "/category shampoo"
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = ["shampoo"]
    
    await category_command(update, context)
    
    update.message.reply_text.assert_called()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bot.py -v`
Expected: FAIL

- [ ] **Step 3: Implement category commands in bot.py**

Add to bot.py:
```python
from categories import CATEGORIES, search_by_category

async def categories_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = ["Доступные категории:\n"]
    for key, cat in CATEGORIES.items():
        lines.append(f"{cat['emoji']} /{key} - {cat['name']}")
    await update.message.reply_text("\n".join(lines))

async def category_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Использование: /category <название>")
        return
    
    category = context.args[0].lower()
    if category not in CATEGORIES:
        await update.message.reply_text("Категория не найдена. Используйте /categories")
        return
    
    await update.message.reply_text("Ищу в категории " + CATEGORIES[category]["name"] + "...")
    
    results = await asyncio.to_thread(search.search_all_stores, CATEGORIES[category]["keywords"][0])
    response = search.format_results(results)
    await update.message.reply_text(response)
```

Register handlers in main():
```python
application.add_handler(CommandHandler("categories", categories_command))
application.add_handler(CommandHandler("category", category_command))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_bot.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add price-compare-bot/bot.py price-compare-bot/tests/test_bot.py
git commit -m "feat: add category bot commands"
```

---

## Task 3: Price History Tracking

**Covers:** Price charts feature

**Files:**
- Modify: `price-compare-bot/database.py`
- Create: `price-compare-bot/price_history.py`
- Create: `price-compare-bot/tests/test_price_history.py`

**Interfaces:**
- Consumes: database.py, search.py
- Produces: `save_price(product, store, price, url)`, `get_price_history(product)`, `get_price_trend(product)`

- [ ] **Step 1: Write failing test**

```python
# tests/test_price_history.py
import pytest
import asyncio
from price_history import PriceHistory

@pytest.fixture
def history():
    return PriceHistory(":memory:")

@pytest.mark.asyncio
async def test_save_price(history):
    await history.connect()
    await history.save_price("Dove гель", "Ozon", 189.0, "https://ozon.ru/123")
    prices = await history.get_price_history("Dove гель")
    assert len(prices) == 1
    assert prices[0]["price"] == 189.0
    await history.close()

@pytest.mark.asyncio
async def test_price_trend(history):
    await history.connect()
    await history.save_price("Dove гель", "Ozon", 215.0, "https://ozon.ru/123")
    await history.save_price("Dove гель", "Ozon", 189.0, "https://ozon.ru/123")
    trend = await history.get_price_trend("Dove гель")
    assert trend["current"] == 189.0
    assert trend["min"] == 189.0
    assert trend["max"] == 215.0
    await history.close()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_price_history.py -v`
Expected: FAIL

- [ ] **Step 3: Implement price_history.py**

```python
# price_history.py
import aiosqlite
from typing import List, Dict, Optional

class PriceHistory:
    def __init__(self, db_path: str = "price_history.db"):
        self.db_path = db_path
        self.conn = None

    async def connect(self):
        self.conn = await aiosqlite.connect(self.db_path)
        await self._create_tables()

    async def _create_tables(self):
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT NOT NULL,
                store TEXT NOT NULL,
                price REAL NOT NULL,
                url TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await self.conn.commit()

    async def save_price(self, product: str, store: str, price: float, url: str):
        await self.conn.execute(
            "INSERT INTO price_history (product, store, price, url) VALUES (?, ?, ?, ?)",
            (product, store, price, url)
        )
        await self.conn.commit()

    async def get_price_history(self, product: str, days: int = 30) -> List[Dict]:
        cursor = await self.conn.execute(
            "SELECT store, price, url, recorded_at FROM price_history WHERE product = ? ORDER BY recorded_at DESC",
            (product,)
        )
        rows = await cursor.fetchall()
        return [{"store": r[0], "price": r[1], "url": r[2], "date": r[3]} for r in rows]

    async def get_price_trend(self, product: str) -> Dict:
        history = await self.get_price_history(product)
        if not history:
            return {"current": 0, "min": 0, "max": 0, "trend": "unknown"}
        
        prices = [h["price"] for h in history]
        current = prices[0]
        min_price = min(prices)
        max_price = max(prices)
        
        if len(prices) >= 2:
            if prices[0] < prices[1]:
                trend = "down"
            elif prices[0] > prices[1]:
                trend = "up"
            else:
                trend = "stable"
        else:
            trend = "new"
        
        return {"current": current, "min": min_price, "max": max_price, "trend": trend}

    async def close(self):
        if self.conn:
            await self.conn.close()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_price_history.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add price-compare-bot/price_history.py price-compare-bot/tests/test_price_history.py
git commit -m "feat: add price history tracking"
```

---

## Task 4: Price History Bot Commands

**Covers:** Price charts feature

**Files:**
- Modify: `price-compare-bot/bot.py`
- Modify: `price-compare-bot/tests/test_bot.py`

**Interfaces:**
- Consumes: price_history.py, search.py
- Produces: `/history <product>`, `/trend <product>` commands

- [ ] **Step 1: Write failing test**

```python
# Add to tests/test_bot.py
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from bot import history_command, trend_command

@pytest.mark.asyncio
@patch('search.search_all_stores')
async def test_history_command(mock_search):
    mock_search.return_value = [{"name": "Dove гель", "price": 189, "url": "test.ru", "store": "Ozon"}]
    update = MagicMock()
    update.message.text = "/history Dove гель"
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = ["Dove", "гель"]
    
    await history_command(update, context)
    
    update.message.reply_text.assert_called()

@pytest.mark.asyncio
@patch('search.search_all_stores')
async def test_trend_command(mock_search):
    mock_search.return_value = [{"name": "Dove гель", "price": 189, "url": "test.ru", "store": "Ozon"}]
    update = MagicMock()
    update.message.text = "/trend Dove гель"
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = ["Dove", "гель"]
    
    await trend_command(update, context)
    
    update.message.reply_text.assert_called()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bot.py -v`
Expected: FAIL

- [ ] **Step 3: Implement history commands in bot.py**

Add to bot.py:
```python
from price_history import PriceHistory

price_db = PriceHistory()

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Использование: /history <название товара>")
        return
    
    product = " ".join(context.args)
    await price_db.connect()
    history = await price_db.get_price_history(product)
    await price_db.close()
    
    if not history:
        await update.message.reply_text("История цен не найдена для: " + product)
        return
    
    lines = ["История цен для " + product + ":\n"]
    for h in history[:10]:
        lines.append(f"• {h['store']} - {h['price']} руб ({h['date'][:10]})")
    
    await update.message.reply_text("\n".join(lines))

async def trend_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Использование: /trend <название товара>")
        return
    
    product = " ".join(context.args)
    await price_db.connect()
    trend = await price_db.get_price_trend(product)
    await price_db.close()
    
    if trend["current"] == 0:
        await update.message.reply_text("Данные не найдены для: " + product)
        return
    
    trend_emoji = "📈" if trend["trend"] == "up" else "📉" if trend["trend"] == "down" else "➡️"
    
    text = (
        f"Тренд цен для {product}:\n\n"
        f"{trend_emoji} Текущая цена: {trend['current']} руб\n"
        f"📊 Минимум: {trend['min']} руб\n"
        f"📊 Максимум: {trend['max']} руб\n"
        f"📈 Тренд: {trend['trend']}"
    )
    
    await update.message.reply_text(text)
```

Register handlers in main():
```python
application.add_handler(CommandHandler("history", history_command))
application.add_handler(CommandHandler("trend", trend_command))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_bot.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add price-compare-bot/bot.py price-compare-bot/tests/test_bot.py
git commit -m "feat: add price history bot commands"
```

---

## Task 5: Sale Notifications

**Covers:** Sale notifications feature

**Files:**
- Create: `price-compare-bot/notifications.py`
- Create: `price-compare-bot/tests/test_notifications.py`

**Interfaces:**
- Consumes: price_history.py, search.py
- Produces: `check_sales()`, `format_sale_notification(sale)`

- [ ] **Step 1: Write failing test**

```python
# tests/test_notifications.py
import pytest
from notifications import check_sales, format_sale_notification

def test_format_sale_notification():
    sale = {
        "product": "Dove гель",
        "store": "Ozon",
        "old_price": 215.0,
        "new_price": 189.0,
        "url": "https://ozon.ru/123"
    }
    text = format_sale_notification(sale)
    assert "Dove гель" in text
    assert "189" in text
    assert "215" in text
    assert "Ozon" in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_notifications.py -v`
Expected: FAIL

- [ ] **Step 3: Implement notifications.py**

```python
# notifications.py
from price_history import PriceHistory
from typing import List, Dict

async def check_sales(threshold: float = 10.0) -> List[Dict]:
    db = PriceHistory()
    await db.connect()
    
    # Get all tracked products
    cursor = await db.conn.execute(
        "SELECT DISTINCT product FROM price_history"
    )
    products = [row[0] for row in await cursor.fetchall()]
    
    sales = []
    for product in products:
        trend = await db.get_price_trend(product)
        if trend["current"] > 0 and trend["min"] > 0:
            decrease = ((trend["max"] - trend["current"]) / trend["max"]) * 100
            if decrease >= threshold:
                sales.append({
                    "product": product,
                    "store": "Разные магазины",
                    "old_price": trend["max"],
                    "new_price": trend["current"],
                    "url": "",
                    "decrease": decrease
                })
    
    await db.close()
    return sales

def format_sale_notification(sale: Dict) -> str:
    decrease = sale.get("decrease", 0)
    return (
        "СКИДКА!\n\n"
        f"Товар: {sale['product']}\n"
        f"Магазин: {sale['store']}\n"
        f"Было: {sale['old_price']} руб\n"
        f"Стало: {sale['new_price']} руб\n"
        f"Скидка: {decrease:.0f}%\n"
        f"Ссылка: {sale['url']}"
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_notifications.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add price-compare-bot/notifications.py price-compare-bot/tests/test_notifications.py
git commit -m "feat: add sale notifications"
```

---

## Task 6: Sale Notifications Bot Commands

**Covers:** Sale notifications feature

**Files:**
- Modify: `price-compare-bot/bot.py`
- Modify: `price-compare-bot/tests/test_bot.py`

**Interfaces:**
- Consumes: notifications.py
- Produces: `/sales`, `/track_sale <product>` commands

- [ ] **Step 1: Write failing test**

```python
# Add to tests/test_bot.py
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from bot import sales_command

@pytest.mark.asyncio
@patch('notifications.check_sales')
async def test_sales_command(mock_check):
    mock_check.return_value = [{
        "product": "Dove гель",
        "store": "Ozon",
        "old_price": 215.0,
        "new_price": 189.0,
        "url": "https://ozon.ru/123",
        "decrease": 12.0
    }]
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    
    await sales_command(update, context)
    
    update.message.reply_text.assert_called()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bot.py -v`
Expected: FAIL

- [ ] **Step 3: Implement sales command in bot.py**

Add to bot.py:
```python
from notifications import check_sales, format_sale_notification

async def sales_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Проверяю скидки...")
    
    sales = await asyncio.to_thread(check_sales, 10.0)
    
    if not sales:
        await update.message.reply_text("Активных скидок не найдено")
        return
    
    for sale in sales[:5]:
        text = format_sale_notification(sale)
        await update.message.reply_text(text)
```

Register handler in main():
```python
application.add_handler(CommandHandler("sales", sales_command))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_bot.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add price-compare-bot/bot.py price-compare-bot/tests/test_bot.py
git commit -m "feat: add sale notifications bot command"
```

---

## Task 7: Price History Auto-Collection

**Covers:** Price charts feature

**Files:**
- Modify: `price-compare-bot/search.py`
- Modify: `price-compare-bot/scheduler.py`

**Interfaces:**
- Consumes: price_history.py
- Produces: Auto-save prices after each search

- [ ] **Step 1: Write failing test**

```python
# Add to tests/test_search.py
import pytest
from unittest.mock import patch, MagicMock
from search import search_all_stores

@patch('scrapers.yandex_market.search_yandex_market')
def test_search_saves_prices(mock_ym):
    mock_ym.return_value = [{"name": "Dove", "price": 189, "url": "test.ru", "store": "Яндекс.Маркет"}]
    results = search_all_stores("Dove", save_history=True)
    assert len(results) > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_search.py -v`
Expected: FAIL

- [ ] **Step 3: Modify search_all_stores to save prices**

Update search.py:
```python
from price_history import PriceHistory

price_db = PriceHistory()

def search_all_stores(query: str, save_history: bool = False) -> List[Dict]:
    # ... existing code ...
    
    if save_history:
        import asyncio
        loop = asyncio.new_event_loop()
        loop.run_until_complete(price_db.connect())
        for r in all_results:
            if r.get("price", 0) > 0:
                loop.run_until_complete(price_db.save_price(query, r["store"], r["price"], r["url"]))
        loop.run_until_complete(price_db.close())
        loop.close()
    
    return all_results
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_search.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add price-compare-bot/search.py price-compare-bot/scheduler.py
git commit -m "feat: auto-save prices after search"
```

---

## Summary

| Task | Description | Dependencies |
|------|-------------|--------------|
| 1 | Category system | None |
| 2 | Category bot commands | Task 1 |
| 3 | Price history tracking | None |
| 4 | Price history bot commands | Task 3 |
| 5 | Sale notifications | Task 3 |
| 6 | Sale notifications bot commands | Task 5 |
| 7 | Price history auto-collection | Task 3 |

**Estimated time:** 2-3 hours for experienced developer
