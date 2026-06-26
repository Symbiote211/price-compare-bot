CATEGORIES = {
    "shampoo": {
        "name": "Шампуни",
        "keywords": ["шампунь", "шампунь для волос", "shampoo", "shampooing"],
        "emoji": "🧴"
    },
    "cream": {
        "name": "Кремы",
        "keywords": ["крем", "крем для лица", "крем для рук", "cream", "crema"],
        "emoji": "🫧"
    },
    "gel": {
        "name": "Гели",
        "keywords": ["гель", "гель для душа", "гель для волос", "gel", "gel douche"],
        "emoji": "💧"
    },
    "deodorant": {
        "name": "Дезодоранты",
        "keywords": ["дезодорант", "антиперспирант", "deodorant", "anti-perspirant"],
        "emoji": "🫶"
    },
    "perfume": {
        "name": "Парфюмерия",
        "keywords": ["парфюм", "духи", "туалетная вода", "parfum", "eau de toilette", "eau de parfum"],
        "emoji": "🌸"
    },
    "makeup": {
        "name": "Макияж",
        "keywords": ["помада", "тушь", "тональный крем", "пудра", "makeup", "lipstick", "mascara"],
        "emoji": "💄"
    }
}


def get_category_products(category: str) -> dict | None:
    return CATEGORIES.get(category)


def search_by_category(query: str, category: str) -> bool:
    cat = CATEGORIES.get(category)
    if not cat:
        return False
    query_lower = query.lower()
    return any(kw.lower() in query_lower for kw in cat["keywords"])
