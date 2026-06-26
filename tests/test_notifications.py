import pytest
from notifications import check_sales, format_sale_notification


@pytest.fixture
def sample_prices():
    return [
        {"product": "Laptop", "store": "Store A", "price": 900.0, "recorded_at": "2024-01-02"},
        {"product": "Laptop", "store": "Store A", "price": 1000.0, "recorded_at": "2024-01-01"},
    ]


@pytest.fixture
def sale_notification():
    return {
        "product": "Laptop",
        "store": "Store A",
        "current_price": 900.0,
        "previous_price": 1000.0,
        "drop_amount": 100.0,
        "drop_percent": 10.0,
        "recorded_at": "2024-01-02",
        "url": "https://example.com/laptop"
    }


class TestCheckSales:
    def test_no_sales_when_prices_same(self):
        prices = [
            {"product": "Phone", "store": "Store B", "price": 500.0, "recorded_at": "2024-01-02"},
            {"product": "Phone", "store": "Store B", "price": 500.0, "recorded_at": "2024-01-01"},
        ]
        assert check_sales(prices, 0.1) == []

    def test_no_sales_below_threshold(self):
        prices = [
            {"product": "Phone", "store": "Store B", "price": 490.0, "recorded_at": "2024-01-02"},
            {"product": "Phone", "store": "Store B", "price": 500.0, "recorded_at": "2024-01-01"},
        ]
        assert check_sales(prices, 0.1) == []

    def test_detects_sale(self, sample_prices):
        sales = check_sales(sample_prices, 0.1)
        assert len(sales) == 1
        assert sales[0]["drop_percent"] == 10.0

    def test_empty_history(self):
        assert check_sales([], 0.1) == []

    def test_single_price(self):
        prices = [{"product": "X", "store": "S", "price": 100.0, "recorded_at": "2024-01-01"}]
        assert check_sales(prices, 0.1) == []


class TestFormatSaleNotification:
    def test_format_with_url(self, sale_notification):
        result = format_sale_notification(sale_notification)
        assert "SALE ALERT!" in result
        assert "$900.00" in result
        assert "$100.00" in result
        assert "https://example.com/laptop" in result

    def test_format_without_url(self, sale_notification):
        del sale_notification["url"]
        result = format_sale_notification(sale_notification)
        assert "Link:" not in result