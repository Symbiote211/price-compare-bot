import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from search import search_all_stores

@patch('scrapers.aliexpress.search_aliexpress', return_value=[])
@patch('scrapers.apteka366.search_apteka366', return_value=[])
@patch('scrapers.svyetofor.search_svyetofor', return_value=[])
@patch('scrapers.iledebeaute.search_iledebeaute', return_value=[])
@patch('scrapers.rivgosh.search_rivgosh', return_value=[])
@patch('scrapers.magnit_cosmetic.search_magnit_cosmetic', return_value=[])
@patch('scrapers.podruzka.search_podruzka', return_value=[])
@patch('scrapers.letual.search_letual', return_value=[])
@patch('scrapers.goldapple.search_goldapple', return_value=[])
@patch('scrapers.yandex_market.search_yandex_market', return_value=[])
@patch('scrapers.ozon.search_ozon')
@patch('scrapers.wildberries.search_wildberries')
def test_search_all_stores(mock_wb, mock_ozon, mock_ym, mock_ga, mock_lt,
                           mock_pr, mock_mc, mock_rg, mock_idb, mock_sv,
                           mock_apt, mock_ae):
    mock_wb.return_value = [{"name": "Dove WB", "price": 189, "url": "wb.ru/1", "store": "Wildberries"}]
    mock_ozon.return_value = [{"name": "Dove Ozon", "price": 199, "url": "ozon.ru/1", "store": "Ozon"}]
    mock_ym.return_value = [{"name": "Dove YM", "price": 209, "url": "ym.ru/1", "store": "Яндекс.Маркет"}]
    
    results = search_all_stores("Dove гель")
    assert len(results) == 3
    assert results[0]["price"] <= results[1]["price"] <= results[2]["price"]

@patch('scrapers.aliexpress.search_aliexpress', return_value=[])
@patch('scrapers.apteka366.search_apteka366', return_value=[])
@patch('scrapers.svyetofor.search_svyetofor', return_value=[])
@patch('scrapers.iledebeaute.search_iledebeaute', return_value=[])
@patch('scrapers.rivgosh.search_rivgosh', return_value=[])
@patch('scrapers.magnit_cosmetic.search_magnit_cosmetic', return_value=[])
@patch('scrapers.podruzka.search_podruzka', return_value=[])
@patch('scrapers.letual.search_letual', return_value=[])
@patch('scrapers.goldapple.search_goldapple', return_value=[])
@patch('scrapers.yandex_market.search_yandex_market', return_value=[])
@patch('scrapers.ozon.search_ozon')
@patch('scrapers.wildberries.search_wildberries')
def test_search_saves_prices_when_save_history_true(mock_wb, mock_ozon, mock_ym, mock_ga, mock_lt,
                                                    mock_pr, mock_mc, mock_rg, mock_idb, mock_sv,
                                                    mock_apt, mock_ae):
    mock_wb.return_value = [{"name": "Dove WB", "price": 189, "url": "wb.ru/1", "store": "Wildberries"}]
    mock_ozon.return_value = [{"name": "Dove Ozon", "price": 199, "url": "ozon.ru/1", "store": "Ozon"}]
    mock_ym.return_value = [{"name": "Dove YM", "price": 209, "url": "ym.ru/1", "store": "Яндекс.Маркет"}]

    mock_history = MagicMock()
    mock_history.connect = AsyncMock()
    mock_history.save_price = AsyncMock()
    mock_history.close = AsyncMock()

    with patch('search.PriceHistory', return_value=mock_history):
        results = search_all_stores("Dove гель", save_history=True)

    assert len(results) == 3
    assert mock_history.connect.called
    assert mock_history.save_price.call_count == 3
    assert mock_history.close.called

@patch('scrapers.aliexpress.search_aliexpress', return_value=[])
@patch('scrapers.apteka366.search_apteka366', return_value=[])
@patch('scrapers.svyetofor.search_svyetofor', return_value=[])
@patch('scrapers.iledebeaute.search_iledebeaute', return_value=[])
@patch('scrapers.rivgosh.search_rivgosh', return_value=[])
@patch('scrapers.magnit_cosmetic.search_magnit_cosmetic', return_value=[])
@patch('scrapers.podruzka.search_podruzka', return_value=[])
@patch('scrapers.letual.search_letual', return_value=[])
@patch('scrapers.goldapple.search_goldapple', return_value=[])
@patch('scrapers.yandex_market.search_yandex_market', return_value=[])
@patch('scrapers.ozon.search_ozon')
@patch('scrapers.wildberries.search_wildberries')
def test_search_no_save_when_save_history_false(mock_wb, mock_ozon, mock_ym, mock_ga, mock_lt,
                                                mock_pr, mock_mc, mock_rg, mock_idb, mock_sv,
                                                mock_apt, mock_ae):
    mock_wb.return_value = [{"name": "Dove WB", "price": 189, "url": "wb.ru/1", "store": "Wildberries"}]
    mock_ozon.return_value = [{"name": "Dove Ozon", "price": 199, "url": "ozon.ru/1", "store": "Ozon"}]

    with patch('search.PriceHistory') as mock_history_cls:
        results = search_all_stores("Dove гель", save_history=False)

    assert len(results) == 2
    assert not mock_history_cls.called
