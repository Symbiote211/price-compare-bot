import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from bot import handle_message, handle_photo, list_categories, category_search

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
