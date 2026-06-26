import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from bot import handle_message, handle_photo, list_categories, category_search, price_history_command, price_trend_command

@pytest.mark.asyncio
@patch('search.search_all_stores')
async def test_handle_message(mock_search):
    mock_search.return_value = [{"name": "Dove", "price": 189, "url": "test.ru", "store": "Ozon"}]
    update = MagicMock()
    update.message.text = "Dove гель"
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    
    await handle_message(update, context)

    assert update.message.reply_text.call_count >= 1

@pytest.mark.asyncio
@patch('image_recognizer.recognize_product')
@patch('search.search_all_stores')
async def test_handle_photo(mock_search, mock_recognize):
    mock_recognize.return_value = "Dove гель для душа"
    mock_search.return_value = [{"name": "Dove", "price": 189, "url": "test.ru", "store": "Ozon"}]
    
    update = MagicMock()
    photo = MagicMock()
    photo.file_id = "test_file_id"
    update.message.photo = [photo]
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.bot.get_file = AsyncMock(return_value=MagicMock(download_as_bytearray=AsyncMock()))
    
    await handle_photo(update, context)
    
    update.message.reply_text.assert_called_once()

@pytest.mark.asyncio
async def test_list_categories():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    
    await list_categories(update, context)
    
    update.message.reply_text.assert_called_once()
    reply_text = update.message.reply_text.call_args[0][0]
    assert "🧴" in reply_text
    assert "Шампуни" in reply_text
    assert "Кремы" in reply_text

@pytest.mark.asyncio
@patch('search.search_all_stores')
async def test_category_search(mock_search):
    mock_search.return_value = [{"name": "Shampoo", "price": 299, "url": "test.ru", "store": "Ozon"}]
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = ["шампуни"]
    
    await category_search(update, context)
    
    assert update.message.reply_text.call_count >= 2

@pytest.mark.asyncio
async def test_category_search_no_args():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = []
    
    await category_search(update, context)
    
    update.message.reply_text.assert_called_once()
    reply_text = update.message.reply_text.call_args[0][0]
    assert "Использование" in reply_text

@pytest.mark.asyncio
async def test_category_search_invalid():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = ["несуществующая"]
    
    await category_search(update, context)
    
    update.message.reply_text.assert_called_once()
    reply_text = update.message.reply_text.call_args[0][0]
    assert "не найдена" in reply_text

@pytest.mark.asyncio
async def test_price_history_command():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = ["Dove гель"]

    mock_history = MagicMock()
    mock_history.get_price_history = AsyncMock(return_value=[
        {"store": "Ozon", "price": 189, "url": "test.ru", "recorded_at": "2025-01-15 10:00:00"},
        {"store": "Wildberries", "price": 199, "url": "test2.ru", "recorded_at": "2025-01-14 10:00:00"}
    ])
    mock_history.connect = AsyncMock()
    mock_history.close = AsyncMock()

    with patch('bot.PriceHistory', return_value=mock_history):
        await price_history_command(update, context)

    assert update.message.reply_text.call_count >= 1
    reply_text = update.message.reply_text.call_args[0][0]
    assert "189" in reply_text
    assert "Ozon" in reply_text

@pytest.mark.asyncio
async def test_price_history_no_args():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = []

    await price_history_command(update, context)

    update.message.reply_text.assert_called_once()
    reply_text = update.message.reply_text.call_args[0][0]
    assert "Использование" in reply_text

@pytest.mark.asyncio
async def test_price_history_no_data():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = ["Неизвестный товар"]

    mock_history = MagicMock()
    mock_history.get_price_history = AsyncMock(return_value=[])
    mock_history.connect = AsyncMock()
    mock_history.close = AsyncMock()

    with patch('bot.PriceHistory', return_value=mock_history):
        await price_history_command(update, context)

    update.message.reply_text.assert_called_once()
    reply_text = update.message.reply_text.call_args[0][0]
    assert "Нет истории цен" in reply_text

@pytest.mark.asyncio
async def test_price_trend_command():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = ["Dove гель"]

    mock_history = MagicMock()
    mock_history.get_price_trend = AsyncMock(return_value={
        "current": 189,
        "min": 179,
        "max": 199,
        "trend": "decreasing"
    })
    mock_history.connect = AsyncMock()
    mock_history.close = AsyncMock()

    with patch('bot.PriceHistory', return_value=mock_history):
        await price_trend_command(update, context)

    assert update.message.reply_text.call_count >= 1
    reply_text = update.message.reply_text.call_args[0][0]
    assert "189" in reply_text
    assert "📉" in reply_text
    assert "decreasing" in reply_text

@pytest.mark.asyncio
async def test_price_trend_no_args():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = []

    await price_trend_command(update, context)

    update.message.reply_text.assert_called_once()
    reply_text = update.message.reply_text.call_args[0][0]
    assert "Использование" in reply_text

@pytest.mark.asyncio
async def test_price_trend_no_data():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = ["Неизвестный товар"]

    mock_history = MagicMock()
    mock_history.get_price_trend = AsyncMock(return_value={
        "current": None,
        "min": None,
        "max": None,
        "trend": "unknown"
    })
    mock_history.connect = AsyncMock()
    mock_history.close = AsyncMock()

    with patch('bot.PriceHistory', return_value=mock_history):
        await price_trend_command(update, context)

    update.message.reply_text.assert_called_once()
    reply_text = update.message.reply_text.call_args[0][0]
    assert "Нет данных" in reply_text
