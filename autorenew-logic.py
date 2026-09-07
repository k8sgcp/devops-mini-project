from datetime import datetime
from dateutil.relativedelta import relativedelta

# Constants
RENEWAL_FEE = 99.00
RENEWAL_PERIOD_MONTHS = 3


def process_gold_auto_renewal(user_id, account_balance, has_digital_consent):
    """Handles auto-renewal of Gold membership every 3 months for Rs 99."""
    # Step 1: Verify valid digital consent
    if not has_digital_consent:
        return {
            "status": "FAILED",
            "message": "User consent not found for auto-renewal.",
        }

    # Step 2: Verify sufficient balance
    if account_balance < RENEWAL_FEE:
        return {
            "status": "FAILED",
            "message": f"Insufficient funds. Required: Rs {RENEWAL_FEE}",
        }

    # Step 3: Deduct payment and compute new expiration date
    new_balance = account_balance - RENEWAL_FEE
    current_time = datetime.now()
    new_expiry_date = current_time + relativedelta(months=RENEWAL_PERIOD_MONTHS)

    return {
        "status": "SUCCESS",
        "user_id": user_id,
        "amount_deducted": RENEWAL_FEE,
        "remaining_balance": new_balance,
        "renewal_date": current_time.strftime("%Y-%m-%d"),
        "new_expiry_date": new_expiry_date.strftime("%Y-%m-%d"),
    }


# Example execution:
user_data = {"user_id": "usr_98765", "balance": 250.00, "consent": True}

result = process_gold_auto_renewal(
    user_id=user_data["user_id"],
    account_balance=user_data["balance"],
    has_digital_consent=user_data["consent"],
)

print(result)
