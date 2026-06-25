import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from scheduler import check_tracked_prices, format_price_drop_notification


@pytest.mark.asyncio
@patch('scheduler.Database')
async def test_check_prices(mock_db_cls):
    mock_db = AsyncMock()
    mock_db_cls.return_value = mock_db
    mock_db.get_all_tracked_users.return_value = [1]
    mock_db.get_tracked_products.return_value = [{"id": 1, "product_name": "Dove"}]
    mock_db.check_price_drops.return_value = [
        {"product_name": "Dove", "store": "Ozon", "old_price": 215, "new_price": 189, "url": "test.ru"}
    ]

    with patch('scheduler.search_all_stores') as mock_search:
        mock_search.return_value = [
            {"store": "Ozon", "price": 189, "url": "test.ru", "name": "Dove"}
        ]
        updates = await check_tracked_prices()

    assert len(updates) == 1
    assert updates[0]["product_name"] == "Dove"
    mock_db.connect.assert_awaited_once()
    mock_db.close.assert_awaited_once()


def test_format_price_drop_notification():
    drop = {
        "product_name": "Dove",
        "store": "Ozon",
        "old_price": 215,
        "new_price": 189,
        "url": "https://ozon.ru/dove"
    }
    msg = format_price_drop_notification(drop)
    assert "Dove" in msg
    assert "215" in msg
    assert "189" in msg
    assert "Ozon" in msg
    assert "https://ozon.ru/dove" in msg
    assert "12%" in msg
