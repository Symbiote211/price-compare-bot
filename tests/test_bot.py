import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from bot import handle_message, handle_photo

@pytest.mark.asyncio
@patch('search.search_all_stores')
async def test_handle_message(mock_search):
    mock_search.return_value = [{"name": "Dove", "price": 189, "url": "test.ru", "store": "Ozon"}]
    update = MagicMock()
    update.message.text = "Dove гель"
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    
    await handle_message(update, context)
    
    update.message.reply_text.assert_called_once()

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
