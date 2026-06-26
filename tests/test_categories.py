from categories import CATEGORIES, get_category_products, search_by_category


def test_categories_count():
    assert len(CATEGORIES) == 6


def test_categories_have_required_keys():
    for cat in CATEGORIES.values():
        assert "name" in cat
        assert "keywords" in cat
        assert "emoji" in cat
        assert isinstance(cat["keywords"], list)
        assert len(cat["keywords"]) > 0


def test_get_category_products_found():
    result = get_category_products("shampoo")
    assert result is not None
    assert result["name"] == "Шампуни"


def test_get_category_products_not_found():
    result = get_category_products("nonexistent")
    assert result is None


def test_search_by_category_match():
    assert search_by_category("shampoo для детей", "shampoo") is True
    assert search_by_category("крем для лица", "cream") is True
    assert search_by_category("гель для душа Dove", "gel") is True
    assert search_by_category("дезодорант Nivea", "deodorant") is True
    assert search_by_category("парфюм Chanel", "perfume") is True
    assert search_by_category("тушь для ресниц", "makeup") is True


def test_search_by_category_no_match():
    assert search_by_category("сок апельсиновый", "shampoo") is False


def test_search_by_category_invalid_category():
    assert search_by_category("шампунь", "nonexistent") is False


def test_search_by_category_case_insensitive():
    assert search_by_category("ШАМПУНЬ", "shampoo") is True
