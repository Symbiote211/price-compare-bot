import aiosqlite
from datetime import datetime, timedelta
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

    async def save_price(self, product: str, store: str, price: float, url: str = None):
        await self.conn.execute(
            "INSERT INTO price_history (product, store, price, url) VALUES (?, ?, ?, ?)",
            (product, store, price, url)
        )
        await self.conn.commit()

    async def get_price_history(self, product: str, days: int = 30) -> List[Dict]:
        cursor = await self.conn.execute(
            """SELECT store, price, url, recorded_at 
               FROM price_history 
               WHERE product = ? AND recorded_at >= datetime('now', ?)
               ORDER BY recorded_at DESC, id DESC""",
            (product, f"-{days} days")
        )
        rows = await cursor.fetchall()
        return [{"store": r[0], "price": r[1], "url": r[2], "recorded_at": r[3]} for r in rows]

    async def get_price_trend(self, product: str) -> Dict:
        history = await self.get_price_history(product)
        if not history:
            return {"current": None, "min": None, "max": None, "trend": "unknown"}
        
        prices = [entry["price"] for entry in history]
        current = prices[0]
        min_price = min(prices)
        max_price = max(prices)
        
        if len(prices) < 2:
            trend = "stable"
        else:
            prev_price = prices[1]
            if current > prev_price:
                trend = "increasing"
            elif current < prev_price:
                trend = "decreasing"
            else:
                trend = "stable"
        
        return {
            "current": current,
            "min": min_price,
            "max": max_price,
            "trend": trend
        }

    async def close(self):
        if self.conn:
            await self.conn.close()