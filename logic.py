from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class PaymentMethod(Enum):
    CREDIT_CARD = "CREDIT_CARD"
    UPI = "UPI"
    NET_BANKING = "NET_BANKING"
    PAY_ON_DELIVERY = "PAY_ON_DELIVERY"


@dataclass
class Item:
    item_id: str
    name: str
    price: float
    quantity: int
    in_stock: bool = True


@dataclass
class Cart:
    items: List[Item] = field(default_factory=list)
    coupon_code: Optional[str] = None

    @property
    def subtotal(self) -> float:
        return sum(item.price * item.quantity for item in self.items)


class CheckoutService:
    TAX_RATE = 0.18  # 18% GST/Tax
    FLAT_SHIPPING_FEE = 50.0
    FREE_SHIPPING_THRESHOLD = 500.0

    VALID_COUPONS = {
        "WELCOME10": 0.10,  # 10% off
        "FLAT100": 100.0,   # Flat 100 off
    }

    def validate_cart(self, cart: Cart) -> None:
        """Ensures cart is valid and items are available in stock."""
        if not cart.items:
            raise ValueError("Cart is empty.")

        for item in cart.items:
            if not item.in_stock:
                raise ValueError(f"Item '{item.name}' is currently out of stock.")
            if item.quantity <= 0:
                raise ValueError(f"Invalid quantity for '{item.name}'.")

    def calculate_discount(self, subtotal: float, coupon_code: Optional[str]) -> float:
        """Calculates discount based on applied coupon code."""
        if not coupon_code or coupon_code not in self.VALID_COUPONS:
            return 0.0

        discount_rule = self.VALID_COUPONS[coupon_code]
        if isinstance(discount_rule, float) and discount_rule < 1.0:
            return subtotal * discount_rule  # Percentage discount
        elif isinstance(discount_rule, float):
            return min(discount_rule, subtotal)  # Flat discount (capped at subtotal)
        return 0.0

    def calculate_shipping(self, discounted_subtotal: float) -> float:
        """Determines shipping fee based on threshold."""
        if discounted_subtotal >= self.FREE_SHIPPING_THRESHOLD:
            return 0.0
        return self.FLAT_SHIPPING_FEE

    def process_payment(self, amount: float, method: PaymentMethod) -> bool:
        """Simulates payment gateway processing."""
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        # Payment integration logic would go here (e.g., Stripe, Razorpay)
        print(f"Processing payment of ₹{amount:.2f} via {method.value}...")
        return True  # Simulating a successful transaction

    def checkout(self, cart: Cart, shipping_address: str, payment_method: PaymentMethod) -> dict:
        """Executes the complete checkout flow."""
        # 1. Validation
        if not shipping_address.strip():
            raise ValueError("Shipping address is required.")
        self.validate_cart(cart)

        # 2. Cost Calculations
        subtotal = cart.subtotal
        discount = self.calculate_discount(subtotal, cart.coupon_code)
        taxable_amount = subtotal - discount
        tax = taxable_amount * self.TAX_RATE
        shipping = self.calculate_shipping(taxable_amount)
        grand_total = taxable_amount + tax + shipping

        # 3. Payment Execution
        payment_successful = self.process_payment(grand_total, payment_method)
        if not payment_successful:
            raise RuntimeError("Payment failed. Order not placed.")

        # 4. Construct Order Receipt
        return {
            "status": "SUCCESS",
            "shipping_address": shipping_address,
            "payment_method": payment_method.value,
            "summary": {
                "subtotal": round(subtotal, 2),
                "discount": round(discount, 2),
                "tax": round(tax, 2),
                "shipping": round(shipping, 2),
                "grand_total": round(grand_total, 2),
            },
        }


# --- Usage Example ---
if __name__ == "__main__":
    # Sample items in cart
    cart_items = [
        Item(item_id="101", name="Wireless Mouse", price=450.0, quantity=1),
        Item(item_id="102", name="USB Cable", price=150.0, quantity=2),
    ]

    user_cart = Cart(items=cart_items, coupon_code="WELCOME10")
    checkout_system = CheckoutService()

    try:
        receipt = checkout_system.checkout(
            cart=user_cart,
            shipping_address="123 Main St, Tech City, 400001",
            payment_method=PaymentMethod.UPI,
        )
        print("\nOrder Placed Successfully!")
        print(receipt)
    except (ValueError, RuntimeError) as e:
        print(f"\nCheckout Failed: {e}")
