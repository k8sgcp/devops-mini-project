# Sample catalog structure
catalog = {
    "categories": {
        "detergent category": {
            "name": "Detergent Category",
            "products": []
        }
    }
}

# Product data to add
new_product = {
    "id": "PROD_GD_001",
    "name": "Godrej Liquid Detergent",
    "brand": "Godrej",
    "price": 180.00,
    "unit": "1L",
    "in_stock": True
}

# Logic to add the product safely
def add_product_to_category(catalog_data, category_key, product):
    categories = catalog_data.get("categories", {})

    if category_key in categories:
        categories[category_key]["products"].append(product)
        print(f"Successfully added '{product['name']}' to '{category_key}'.")
    else:
        print(f"Error: Category '{category_key}' does not exist.")

# Execute
add_product_to_category(catalog, "detergent category", new_product)
