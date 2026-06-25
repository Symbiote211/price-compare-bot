import asyncio
from typing import List, Dict
from scrapers import (
    search_wildberries, search_ozon, search_yandex_market,
    search_goldapple, search_letual, search_podruzka,
    search_magnit_cosmetic, search_rivgosh, search_iledebeaute,
    search_svyetofor, search_apteka366, search_aliexpress
)

def search_all_stores(query: str) -> List[Dict]:
    all_results = []
    
    all_results.extend(search_wildberries(query))
    all_results.extend(search_ozon(query))
    all_results.extend(search_yandex_market(query))
    all_results.extend(search_goldapple(query))
    all_results.extend(search_letual(query))
    all_results.extend(search_podruzka(query))
    all_results.extend(search_magnit_cosmetic(query))
    all_results.extend(search_rivgosh(query))
    all_results.extend(search_iledebeaute(query))
    all_results.extend(search_svyetofor(query))
    all_results.extend(search_apteka366(query))
    all_results.extend(search_aliexpress(query))
    
    all_results.sort(key=lambda x: x["price"])
    
    return all_results

def format_results(results: List[Dict], top_n: int = 3) -> str:
    if not results:
        return "❌ Товары не найдены"
    
    lines = [f"🔍 Найдено {len(results)} вариантов:\n"]
    
    for i, r in enumerate(results[:top_n], 1):
        lines.append(f"{i}. {r['store']} — {r['price']}₽")
        lines.append(f"   {r['name'][:50]}")
        lines.append(f"   {r['url']}\n")
    
    return "\n".join(lines)
