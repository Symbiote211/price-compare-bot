import asyncio
from typing import List, Dict
from database import Database
from search import search_all_stores
from config import PRICE_DROP_THRESHOLD


async def check_tracked_prices() -> List[Dict]:
    db = Database()
    await db.connect()

    users = await db.get_all_tracked_users()

    for user_id in users:
        products = await db.get_tracked_products(user_id)

        for product in products:
            results = search_all_stores(product["product_name"])

            for result in results[:3]:
                await db.update_price(
                    product["id"],
                    result["store"],
                    result["price"],
                    result["url"]
                )

    drops = await db.check_price_drops(PRICE_DROP_THRESHOLD)

    await db.close()

    return drops


def format_price_drop_notification(drop: Dict) -> str:
    decrease = ((drop["old_price"] - drop["new_price"]) / drop["old_price"]) * 100

    return (
        f"📉 Цена снизилась!\n\n"
        f"{drop['product_name']}\n"
        f"Было: {drop['old_price']}₽ → Стало: {drop['new_price']}₽ (-{decrease:.0f}%)\n"
        f"Магазин: {drop['store']}\n"
        f"{drop['url']}"
    )
