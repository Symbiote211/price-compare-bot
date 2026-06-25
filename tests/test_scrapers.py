import pytest
from unittest.mock import patch, MagicMock
from scrapers.wildberries import search_wildberries
from scrapers.ozon import search_ozon
from scrapers.yandex_market import search_yandex_market
from scrapers.goldapple import search_goldapple
from scrapers.letual import search_letual
from scrapers.podruzka import search_podruzka
from scrapers.magnit_cosmetic import search_magnit_cosmetic
from scrapers.rivgosh import search_rivgosh
from scrapers.iledebeaute import search_iledebeaute
from scrapers.svyetofor import search_svyetofor
from scrapers.apteka366 import search_apteka366
from scrapers.aliexpress import search_aliexpress


@patch('time.sleep', return_value=None)
@patch('requests.get')
def test_search_wildberries(mock_get, mock_sleep):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '''
    <div class="product-card">
        <a href="/catalog/123/product.aspx" class="product-card__name">Dove гель</a>
        <span class="price">189 ₽</span>
    </div>
    '''
    mock_get.return_value = mock_response

    results = search_wildberries("Dove гель")

    assert isinstance(results, list)
    assert len(results) == 1
    item = results[0]
    assert item["name"] == "Dove гель"
    assert item["price"] == 189.0
    assert isinstance(item["price"], float)
    assert item["store"] == "Wildberries"
    assert item["url"] == "https://www.wildberries.ru/catalog/123/product.aspx"


@patch('time.sleep', return_value=None)
@patch('requests.get')
def test_search_ozon(mock_get, mock_sleep):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '''
    <div class="widget-search-result-container">
        <span class="tsBody500Medium">Ozon Dove гель</span>
        <span class="tsHeadline500Medium">199 ₽</span>
    </div>
    '''
    mock_get.return_value = mock_response

    results = search_ozon("Dove гель")

    assert isinstance(results, list)
    assert len(results) == 1
    item = results[0]
    assert item["name"] == "Ozon Dove гель"
    assert isinstance(item["price"], float)
    assert item["price"] == 199.0
    assert item["store"] == "Ozon"
    assert isinstance(item["url"], str)


@patch('time.sleep', return_value=None)
@patch('requests.get')
def test_search_yandex_market(mock_get, mock_sleep):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '''
    <div data-auto="searchOrganic">
        <span data-auto="snippet-title">Yandex Dove гель</span>
        <span data-auto="price-value">209 ₽</span>
        <a href="https://market.yandex.ru/product/123">link</a>
    </div>
    '''
    mock_get.return_value = mock_response

    results = search_yandex_market("Dove гель")

    assert isinstance(results, list)
    assert len(results) == 1
    item = results[0]
    assert item["name"] == "Yandex Dove гель"
    assert item["price"] == 209.0
    assert isinstance(item["price"], float)
    assert item["store"] == "Яндекс.Маркет"
    assert isinstance(item["url"], str)


@patch('requests.get')
def test_search_goldapple(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<div class="product-card">GA test</div>'
    mock_get.return_value = mock_response
    
    results = search_goldapple("Dove гель")
    assert isinstance(results, list)


@patch('time.sleep', return_value=None)
@patch('requests.get')
def test_search_letual(mock_get, mock_sleep):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '''
    <div class="product-card">
        <a href="/product/letual-dove" class="product-card__name">LT Dove гель</a>
        <span class="price">249 ₽</span>
    </div>
    '''
    mock_get.return_value = mock_response

    results = search_letual("Dove гель")

    assert isinstance(results, list)
    assert len(results) == 1
    item = results[0]
    assert item["name"] == "LT Dove гель"
    assert item["price"] == 249.0
    assert isinstance(item["price"], float)
    assert item["store"] == "Летуаль"
    assert item["url"] == "https://www.letual.ru/product/letual-dove"


@patch('requests.get')
def test_search_podruzka(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<div class="product-card">PR test</div>'
    mock_get.return_value = mock_response
    
    results = search_podruzka("Dove гель")
    assert isinstance(results, list)


@patch('requests.get')
def test_search_magnit_cosmetic(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<div class="product-card">MC test</div>'
    mock_get.return_value = mock_response
    
    results = search_magnit_cosmetic("Dove гель")
    assert isinstance(results, list)


@patch('requests.get')
def test_search_rivgosh(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<div class="product-card">RG test</div>'
    mock_get.return_value = mock_response
    
    results = search_rivgosh("Dove гель")
    assert isinstance(results, list)


@patch('requests.get')
def test_search_iledebeaute(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<div class="product-card">IDB test</div>'
    mock_get.return_value = mock_response
    
    results = search_iledebeaute("Dove гель")
    assert isinstance(results, list)


@patch('requests.get')
def test_search_svyetofor(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<div class="product-card">SV test</div>'
    mock_get.return_value = mock_response
    
    results = search_svyetofor("Dove гель")
    assert isinstance(results, list)


@patch('requests.get')
def test_search_apteka366(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<div class="product-card">366 test</div>'
    mock_get.return_value = mock_response
    
    results = search_apteka366("Dove гель")
    assert isinstance(results, list)


@patch('requests.get')
def test_search_aliexpress(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<div class="product-card">AE test</div>'
    mock_get.return_value = mock_response
    
    results = search_aliexpress("Dove гель")
    assert isinstance(results, list)
