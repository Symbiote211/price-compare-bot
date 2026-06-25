import pytest
from unittest.mock import patch, MagicMock
from search import search_all_stores

@patch('search.search_aliexpress', return_value=[])
@patch('search.search_apteka366', return_value=[])
@patch('search.search_svyetofor', return_value=[])
@patch('search.search_iledebeaute', return_value=[])
@patch('search.search_rivgosh', return_value=[])
@patch('search.search_magnit_cosmetic', return_value=[])
@patch('search.search_podruzka', return_value=[])
@patch('search.search_letual', return_value=[])
@patch('search.search_goldapple', return_value=[])
@patch('search.search_yandex_market')
@patch('search.search_ozon')
@patch('search.search_wildberries')
def test_search_all_stores(mock_wb, mock_ozon, mock_ym, mock_ga, mock_lt,
                           mock_pr, mock_mc, mock_rg, mock_idb, mock_sv,
                           mock_apt, mock_ae):
    mock_wb.return_value = [{"name": "Dove WB", "price": 189, "url": "wb.ru/1", "store": "Wildberries"}]
    mock_ozon.return_value = [{"name": "Dove Ozon", "price": 199, "url": "ozon.ru/1", "store": "Ozon"}]
    mock_ym.return_value = [{"name": "Dove YM", "price": 209, "url": "ym.ru/1", "store": "Яндекс.Маркет"}]
    
    results = search_all_stores("Dove гель")
    assert len(results) == 3
    assert results[0]["price"] <= results[1]["price"] <= results[2]["price"]
