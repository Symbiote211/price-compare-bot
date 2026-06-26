from typing import List, Dict


def check_sales(price_history: List[Dict], threshold: float = 0.1) -> List[Dict]:
    """Check for price drops >= threshold.
    
    Args:
        price_history: List of price entries with 'product', 'store', 'price', 'recorded_at'
        threshold: Minimum price drop percentage (0.1 = 10%)
    
    Returns:
        List of sales (price drops)
    """
    if len(price_history) < 2:
        return []
    
    sales = []
    for i in range(len(price_history) - 1):
        current = price_history[i]
        previous = price_history[i + 1]
        
        if previous["price"] > 0:
            drop_pct = (previous["price"] - current["price"]) / previous["price"]
            if drop_pct >= threshold:
                sales.append({
                    "product": current["product"],
                    "store": current["store"],
                    "current_price": current["price"],
                    "previous_price": previous["price"],
                    "drop_amount": previous["price"] - current["price"],
                    "drop_percent": round(drop_pct * 100, 1),
                    "recorded_at": current["recorded_at"],
                    "url": current.get("url")
                })
    
    return sales


def format_sale_notification(sale: Dict) -> str:
    """Format a sale notification text."""
    url_part = f"\nLink: {sale['url']}" if sale.get("url") else ""
    return (
        f"SALE ALERT!\n\n"
        f"Product: {sale['product']}\n"
        f"Store: {sale['store']}\n"
        f"Current Price: ${sale['current_price']:.2f}\n"
        f"Previous Price: ${sale['previous_price']:.2f}\n"
        f"You Save: ${sale['drop_amount']:.2f} ({sale['drop_percent']}%){url_part}"
    )