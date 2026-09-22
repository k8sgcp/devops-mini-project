from datetime import datetime, date

def calculate_discount(order_amount: float, order_date: date, is_app_order: bool) -> float:
    # Define campaign constraints
    start_date = date(2026, 9, 14)
    end_date = date(2026, 9, 25)
    min_amount = 199.0
    discount_val = 25.0

    # Check all conditions: date range, app source, and order total
    if start_date <= order_date <= end_date and is_app_order and order_amount > min_amount:
        return discount_val

    return 0.0

# --- Example Usage ---
test_order = {
    "amount": 250.0,
    "date": date(2026, 9, 15),
    "is_app": True
}

discount = calculate_discount(test_order["amount"], test_order["date"], test_order["is_app"])
final_price = test_order["amount"] - discount

print(f"Discount Applied: ₹{discount}")
print(f"Final Payable Amount: ₹{final_price}")
