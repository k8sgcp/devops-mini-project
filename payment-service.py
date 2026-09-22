from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PaymentOption:
    id: str
    category: str      # UPI, Cards, NetBanking, COD, PayLater
    title: str
    subtitle: Optional[str] = None
    is_available: bool = True
    badge_offer: Optional[str] = None

class PaymentOptionService:
    def get_payment_page_options(self, user_id: str, cart_value: float) -> dict:
        """
        Simulates fetching and formatting available payment options
        from downstream microservices (User, Offers, Gateway Config).
        """
        # 1. Fetch saved user payment methods (from User Microservice)
        saved_options = [
            PaymentOption("upi_1", "UPI", "GPay (john@okaxis)", subtitle="Saved UPI ID"),
            PaymentOption("card_1", "Cards", "HDFC Credit Card ending in 4021", subtitle="VISA")
        ]

        # 2. Define standard available payment categories (from Payment Gateway Microservice)
        other_options = [
            PaymentOption("upi_intent", "UPI", "Add New UPI ID / App", subtitle="Google Pay, PhonePe, Paytm"),
            PaymentOption("cards", "Cards", "Credit / Debit Cards", subtitle="Visa, Mastercard, RuPay"),
            PaymentOption("netbanking", "NetBanking", "Net Banking", subtitle="All major Indian banks"),
            PaymentOption("paylater", "PayLater", "Simpl / Lazypay", badge_offer="Get ₹50 cashback"),
            PaymentOption("cod", "COD", "Cash on Delivery", is_available=cart_value <= 1000)
        ]

        # 3. Apply promotional rules (from Offers/Promotions Microservice)
        if cart_value >= 500:
            saved_options[1].badge_offer = "10% Instant Discount"

        return {
            "recommended": saved_options,
            "all_options": other_options
        }

def render_payment_page(payment_data: dict):
    """Simulates printing the payment options UI."""
    print("=" * 40)
    print("           SELECT PAYMENT METHOD          ")
    print("=" * 40)

    print("\n[ RECOMMENDED & SAVED METHODS ]")
    for opt in payment_data["recommended"]:
        status = "[AVAILABLE]" if opt.is_available else "[DISABLED]"
        offer = f"  * {opt.badge_offer}" if opt.badge_offer else ""
        print(f" -> {opt.title} ({opt.subtitle}) {offer}")

    print("\n[ OTHER PAYMENT OPTIONS ]")
    for opt in payment_data["all_options"]:
        if not opt.is_available:
            print(f" [X] {opt.title} (Not available for high-value carts)")
            continue

        offer = f"  * {opt.badge_offer}" if opt.badge_offer else ""
        print(f" -> {opt.title} - {opt.subtitle}{offer}")

    print("=" * 40)

# --- Execution ---
if __name__ == "__main__":
    service = PaymentOptionService()

    # Simulating a user checkout with cart value ₹750
    payment_response = service.get_payment_page_options(user_id="usr_9876", cart_value=750.0)
    render_payment_page(payment_response)


# End of file
# This code will be built and tested after local commit and git push via Github Actions workflow
