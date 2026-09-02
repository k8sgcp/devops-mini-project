class InventorySync:
    def __init__(self, low_stock_threshold=5):
        self.low_stock_threshold = low_stock_threshold

    def get_availability_status(self, physical_stock, reserved_stock=0):
        """
        Determine app-facing availability based on physical stock.
        reserved_stock = units already committed to open orders
        """
        available_stock = physical_stock - reserved_stock

        if available_stock <= 0:
            return "OUT_OF_STOCK"
        elif available_stock <= self.low_stock_threshold:
            return "LOW_STOCK"
        else:
            return "IN_STOCK"

    def sync_product(self, product_id, physical_stock, reserved_stock=0):
        status = self.get_availability_status(physical_stock, reserved_stock)
        available_stock = max(physical_stock - reserved_stock, 0)

        return {
            "product_id": product_id,
            "physical_stock": physical_stock,
            "reserved_stock": reserved_stock,
            "available_stock": available_stock,
            "status": status,
            "is_orderable": status != "OUT_OF_STOCK"
        }

    def sync_batch(self, stock_records):
        """
        stock_records: list of dicts like
        {"product_id": "P1", "physical_stock": 12, "reserved_stock": 3}
        """
        return [
            self.sync_product(
                r["product_id"],
                r["physical_stock"],
                r.get("reserved_stock", 0)
            )
            for r in stock_records
        ]


# Example usage
if __name__ == "__main__":
    syncer = InventorySync(low_stock_threshold=5)

    dark_store_stock = [
        {"product_id": "MILK_1L", "physical_stock": 20, "reserved_stock": 2},
        {"product_id": "BREAD_400G", "physical_stock": 3, "reserved_stock": 0},
        {"product_id": "EGGS_12", "physical_stock": 5, "reserved_stock": 5},
    ]

    updates = syncer.sync_batch(dark_store_stock)
    for u in updates:
        print(u)
