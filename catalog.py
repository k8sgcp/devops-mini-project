# Catalog database: indexed by state -> product -> details
CATALOG_BY_REGION = {
    "Maharashtra": {
        "Tomato": {"price_per_kg": 40, "stock": 150, "unit": "kg"},
        "Alphonso Mango": {"price_per_kg": 350, "stock": 50, "unit": "kg"},
        "Spinach": {"price_per_kg": 25, "stock": 80, "unit": "bunch"},
    },
    "West Bengal": {
        "Tomato": {"price_per_kg": 35, "stock": 200, "unit": "kg"},
        "Pointed Gourd (Parwal)": {"price_per_kg": 45, "stock": 100, "unit": "kg"},
        "Jute Leaves (Pat Shak)": {"price_per_kg": 15, "stock": 60, "unit": "bunch"},
    },
}

def get_localized_storefront(customer_state: str):
    """Fetches inventory and pricing tailored to the user's location."""
    # Standardize input string
    formatted_state = customer_state.title().strip()
    
    # Check if region is served
    if formatted_state not in CATALOG_BY_REGION:
        return f"Sorry, service is not available in {customer_state} yet."
    
    inventory = CATALOG_BY_REGION[formatted_state]
    
    # Display available items
    print(f"\n--- Available Products in {formatted_state} ---")
    for item, details in inventory.items():
        print(f"• {item}: ₹{details['price_per_kg']}/{details['unit']} (In Stock: {details['stock']})")

# Example usage
get_localized_storefront("Maharashtra")
get_localized_storefront("West Bengal")
