import time

class QuickCommerceCart:
    def __init__(self, reservation_ttl: int = 300):
        self.reservation_ttl = reservation_ttl  # Expiration time in seconds (300s)
        self.cart_items = []
        self.created_at = None

    def add_item(self, item_name: str, quantity: int, price: float):
        """Adds items to cart and starts/resets the 300-second reservation timer."""
        # Start timer when the first item is added
        if not self.cart_items:
            self.created_at = time.time()

        self.cart_items.append({"item": item_name, "quantity": quantity, "price": price})
        print(f"Added '{item_name}' to cart.")

    def is_expired(self) -> bool:
        """Checks if the 300-second window has passed."""
        if not self.created_at:
            return False

        elapsed_time = time.time() - self.created_at
        return elapsed_time > self.reservation_ttl

    def get_cart(self):
        """Returns active items or clears them if expired."""
        if self.is_expired():
            self._clear_cart("Cart expired! Items discarded due to 300s timeout.")
            return []

        remaining = int(self.reservation_ttl - (time.time() - self.created_at))
        print(f"Cart Active. Time remaining to checkout: {remaining}s")
        return self.cart_items

    def checkout(self) -> bool:
        """Attempts to process checkout."""
        if self.is_expired():
            self._clear_cart("Checkout failed: Reservation window expired.")
            return False

        if not self.cart_items:
            print("Checkout failed: Cart is empty.")
            return False

        print("Checkout successful! Processing payment...")
        self.cart_items = []
        self.created_at = None
        return True

    def _clear_cart(self, reason: str):
        """Internal helper to wipe cart contents."""
        print(f"⚠️ {reason}")
        self.cart_items = []
        self.created_at = None


# ================================
# Example Usage / Simulation
# ================================
if __name__ == "__main__":
    # Create cart with a short TTL (e.g., 3 seconds) for quick testing
    # Change to 300 for actual production limit
    cart = QuickCommerceCart(reservation_ttl=5)

    print("--- 1. User adds items ---")
    cart.add_item("Amul Milk 500ml", 2, 33.00)
    cart.add_item("Bread", 1, 45.00)

    print("\n--- 2. Checking cart immediately ---")
    print("Items in cart:", cart.get_cart())

    print("\n--- 3. Simulating user waiting 6 seconds ---")
    time.sleep(6)

    print("\n--- 4. User attempts checkout after delay ---")
    cart.checkout()


# End of file
