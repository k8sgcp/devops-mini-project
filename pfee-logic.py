class Order:
    PLATFORM_FEE = 25  # Non-refundable fee in INR

    def __init__(self, order_id: str, items_total: float):
        self.order_id = order_id
        self.items_total = items_total
        self.platform_fee = self.PLATFORM_FEE
        self.status = "CREATED"  # Possible: CREATED, PAID, CANCELLED

    @property
    def total_amount(self) -> float:
        """Calculates total bill amount payable by the user."""
        return self.items_total + self.platform_fee

    def process_cancellation((self, reason: str = "User Cancelled") -> dict:
        """
        Handles cancellation and calculates refund.
        Platform fee is strictly excluded from the refund amount.
        """
        if self.status != "PAID":
            raise ValueError("Only paid orders can be refunded.")

        self.status = "CANCELLED"

        refund_amount = self.items_total  # Items total returned; platform fee retained

        return {
            "order_id": self.order_id,
            "status": self.status,
            "reason": reason,
            "items_total": self.items_total,
            "retained_platform_fee": self.platform_fee,
            "refund_amount": refund_amount
        }


# --- Usage Example ---

# 1. Create a new order
my_order = Order(order_id="ORD10092", items_total=1499.00)

print(f"Items Subtotal: ₹{my_order.items_total}")
print(f"Platform Fee:   ₹{my_order.platform_fee}")
print(f"Total Charged:  ₹{my_order.total_amount}")

# 2. Simulate payment
my_order.status = "PAID"

# 3. Simulate order cancellation (delayed, user-cancelled, etc.)
refund_summary = my_order.process_cancellation(reason="Delayed Delivery")

print("\n--- Cancellation Summary ---")
print(f"Refund Issued:  ₹{refund_summary['refund_amount']}")
print(f"Fee Retained:   ₹{refund_summary['retained_platform_fee']}")
