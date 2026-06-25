import aiosqlite
from typing import List, Dict, Optional
from config import DATABASE_PATH

class Database:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.conn = None

    async def connect(self):
        self.conn = await aiosqlite.connect(self.db_path)
        await self._create_tables()

    async def _create_tables(self):
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tracked_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                store TEXT NOT NULL,
                price REAL NOT NULL,
                url TEXT,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES tracked_products(id)
            )
        """)
        await self.conn.commit()

    async def add_tracked_product(self, user_id: int, product_name: str) -> int:
        cursor = await self.conn.execute(
            "INSERT INTO tracked_products (user_id, product_name) VALUES (?, ?)",
            (user_id, product_name)
        )
        await self.conn.commit()
        return cursor.lastrowid

    async def get_tracked_products(self, user_id: int) -> List[Dict]:
        cursor = await self.conn.execute(
            "SELECT id, product_name, created_at FROM tracked_products WHERE user_id = ?",
            (user_id,)
        )
        rows = await cursor.fetchall()
        return [{"id": r[0], "product_name": r[1], "created_at": r[2]} for r in rows]

    async def update_price(self, product_id: int, store: str, price: float, url: str):
        await self.conn.execute(
            "INSERT INTO price_history (product_id, store, price, url) VALUES (?, ?, ?, ?)",
            (product_id, store, price, url)
        )
        await self.conn.commit()

    async def get_price_history(self, product_id: int) -> List[Dict]:
        cursor = await self.conn.execute(
            "SELECT store, price, url, checked_at FROM price_history WHERE product_id = ? ORDER BY checked_at DESC",
            (product_id,)
        )
        rows = await cursor.fetchall()
        return [{"store": r[0], "price": r[1], "url": r[2], "checked_at": r[3]} for r in rows]

    async def check_price_drops(self, threshold: float = 5.0) -> List[Dict]:
        query = """
            WITH latest_prices AS (
                SELECT product_id, store, price, url,
                       ROW_NUMBER() OVER (PARTITION BY product_id, store ORDER BY checked_at DESC, id DESC) as rn
                FROM price_history
            ),
            previous_prices AS (
                SELECT product_id, store, price as old_price
                FROM latest_prices WHERE rn = 2
            ),
            current_prices AS (
                SELECT product_id, store, price as new_price, url
                FROM latest_prices WHERE rn = 1
            )
            SELECT tp.product_name, pp.store, pp.old_price, cp.new_price, cp.url
            FROM tracked_products tp
            JOIN current_prices cp ON tp.id = cp.product_id
            JOIN previous_prices pp ON cp.product_id = pp.product_id AND cp.store = pp.store
            WHERE ((pp.old_price - cp.new_price) / pp.old_price * 100) >= ?
        """
        cursor = await self.conn.execute(query, (threshold,))
        rows = await cursor.fetchall()
        return [{"product_name": r[0], "store": r[1], "old_price": r[2], "new_price": r[3], "url": r[4]} for r in rows]

    async def get_all_tracked_users(self) -> List[int]:
        cursor = await self.conn.execute(
            "SELECT DISTINCT user_id FROM tracked_products"
        )
        rows = await cursor.fetchall()
        return [r[0] for r in rows]

    async def close(self):
        if self.conn:
            await self.conn.close()