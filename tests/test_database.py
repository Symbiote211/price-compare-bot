import pytest
import pytest_asyncio
from database import Database

@pytest_asyncio.fixture
async def db():
    database = Database(":memory:")
    await database.connect()
    yield database
    await database.close()

@pytest.mark.asyncio
async def test_add_tracked_product(db):
    product_id = await db.add_tracked_product(12345, "Dove гель для душа")
    assert product_id is not None
    products = await db.get_tracked_products(12345)
    assert len(products) == 1
    assert products[0]["product_name"] == "Dove гель для душа"

@pytest.mark.asyncio
async def test_update_price(db):
    product_id = await db.add_tracked_product(12345, "Dove гель")
    await db.update_price(product_id, "Ozon", 189.0, "https://ozon.ru/123")
    history = await db.get_price_history(product_id)
    assert len(history) == 1
    assert history[0]["price"] == 189.0

@pytest.mark.asyncio
async def test_check_price_drops(db):
    product_id = await db.add_tracked_product(12345, "Dove гель")
    await db.update_price(product_id, "Ozon", 215.0, "https://ozon.ru/123")
    await db.update_price(product_id, "Ozon", 189.0, "https://ozon.ru/123")
    drops = await db.check_price_drops()
    assert len(drops) == 1
    assert drops[0]["old_price"] == 215.0
    assert drops[0]["new_price"] == 189.0