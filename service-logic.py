def fetch_category_data(category_slug: str):
    """
    Fetches all sub-categories and their respective products 
    when a user taps on a primary category.
    """
    # Standardize input string
    key = category_slug.lower().strip().replace(" ", "_")
    
    # Direct lookup (O(1) time complexity)
    category_data = catalog.get(key)
    
    if not category_data:
        return {
            "success": False,
            "message": f"Category '{category_slug}' not found.",
            "data": None
        }
    
    # Structure the payload response for frontend consumption
    formatted_subcategories = []
    
    for subcat_name, products in category_data.items():
        formatted_subcategories.append({
            "sub_category_name": subcat_name,
            "product_count": len(products),
            "products": products
        })
        
    return {
        "success": True,
        "category": category_slug,
        "total_subcategories": len(formatted_subcategories),
        "sub_categories": formatted_subcategories
    }
