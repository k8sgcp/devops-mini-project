from datetime import datetime, timedelta
import logging

# Set up logging for transaction tracking
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 1. Mock user database
# Assuming today is 2026-08-31
users = [
    {
        "user_id": "usr_101",
        "name": "Aditya",
        "email": "aditya@example.com",
        "subscription_end": "2026-09-01",  # Expires tomorrow (1 day left)
        "payment_token": "tok_visa_4242",
        "plan": "Adobe Creative Cloud",
        "amount_usd": 90.00,
    },
    {
        "user_id": "usr_102",
        "name": "Bob",
        "email": "bob@example.com",
        "subscription_end": "2026-09-05",  # Expires in 5 days
        "payment_token": "tok_mastercard_8888",
        "plan": "Adobe Creative Cloud",
        "amount_usd": 90.00,
    },
]

def charge_payment_gateway(payment_token: str, amount: float, currency: str) -> bool:
    """
    Simulates charging the user's saved card via a payment processor (e.g., Stripe, Razorpay).
    In production, replace this with an actual API call.
    """
    # Simulate payment processing logic
    print(f"--> Charging card token '{payment_token}': {currency} ${amount:.2f}")
    
    # Return True for success, False for failed charge
    return True

def process_automatic_renewals():
    today = datetime.now().date()
    target_renewal_date = today + timedelta(days=1)  # Exactly 1 day before expiry

    for user in users:
        expiry_date = datetime.strptime(user["subscription_end"], "%Y-%m-%d").date()

        # Trigger renewal 1 day before expiration
        if expiry_date == target_renewal_date:
            logging.info(f"Processing 1-day pre-expiry renewal for user: {user['user_id']}")
            
            # Step A: Charge $90 USD
            payment_success = charge_payment_gateway(
                payment_token=user["payment_token"],
                amount=user["amount_usd"],
                currency="USD"
            )

            if payment_success:
                # Step B: Extend subscription by 1 month (30 days) from current expiry date
                new_expiry_date = expiry_date + timedelta(days=30)
                user["subscription_end"] = new_expiry_date.strftime("%Y-%m-%d")
                
                logging.info(
                    f"SUCCESS: Renewed {user['plan']} for {user['name']}. "
                    f"New expiry date: {user['subscription_end']}"
                )
            else:
                # Step C: Handle payment failure (trigger retry email/grace period)
                logging.error(
                    f"FAILED: Payment failed for {user['name']}. "
                    f"Sending urgent payment update link to {user['email']}."
                )

if __name__ == "__main__":
    process_automatic_renewals()
