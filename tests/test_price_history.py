import pytest
import pytest_asyncio
from price_history import PriceHistory


@pytest_asyncio.fixture
async def price_db():
    db = PriceHistory(":memory:")
    await db.connect()
    yield db
    await db.close()


@pytest.mark.asyncio
async def test_save_price(price_db):
    await price_db.save_price("Dove гель", "Ozon", 189.0, "https://ozon.ru/123")
    history = await price_db.get_price_history("Dove гель")
    assert len(history) == 1
    assert history[0]["price"] == 189.0
    assert history[0]["store"] == "Ozon"


@pytest.mark.asyncio
async def test_get_price_history(price_db):
    await price_db.save_price("Dove гель", "Ozon", 215.0)
    await price_db.save_price("Dove гель", "Ozon", 189.0)
    history = await price_db.get_price_history("Dove гель")
    assert len(history) == 2
    assert history[0]["price"] == 189.0
    assert history[1]["price"] == 215.0


@pytest.mark.asyncio
async def test_get_price_history_with_days_filter(price_db):
    await price_db.save_price("Dove гель", "Ozon", 215.0)
    history = await price_db.get_price_history("Dove гель", days=1)
    assert len(history) == 1


@pytest.mark.asyncio
async def test_get_price_trend(price_db):
    await price_db.save_price("Dove гель", "Ozon", 215.0)
    await price_db.save_price("Dove гель", "Ozon", 189.0)
    trend = await price_db.get_price_trend("Dove гель")
    assert trend["current"] == 189.0
    assert trend["min"] == 189.0
    assert trend["max"] == 215.0
    assert trend["trend"] == "decreasing"


@pytest.mark.asyncio
async def test_get_price_trend_empty_history(price_db):
    trend = await price_db.get_price_trend("Non-existent Product")
    assert trend["current"] is None
    assert trend["min"] is None
    assert trend["max"] is None
    assert trend["trend"] == "unknown"


@pytest.mark.asyncio
async def test_get_price_trend_stable(price_db):
    await price_db.save_price("Dove гель", "Ozon", 189.0)
    await price_db.save_price("Dove гель", "Ozon", 189.0)
    trend = await price_db.get_price_trend("Dove гель")
    assert trend["trend"] == "stable"


@pytest.mark.asyncio
async def test_get_price_trend_increasing(price_db):
    await price_db.save_price("Dove гель", "Ozon", 189.0)
    await price_db.save_price("Dove гель", "Ozon", 215.0)
    trend = await price_db.get_price_trend("Dove гель")
    assert trend["current"] == 215.0
    assert trend["min"] == 189.0
    assert trend["max"] == 215.0
    assert trend["trend"] == "increasing"