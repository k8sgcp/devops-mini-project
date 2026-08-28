# Input parameters
cart_value = 1200.00
coupon_code = "SAVE50"

# Target coupon config
VALID_COUPON = "SAVE50"
DISCOUNT_RATE = 0.50

# Logic
if coupon_code.strip().upper() == VALID_COUPON:
    discount_amount = cart_value * DISCOUNT_RATE
    net_payable = cart_value - discount_amount
    coupon_applied = True
else:
    discount_amount = 0.0
    net_payable = cart_value
    coupon_applied = False

# Next Screen / Output Display
print("--- ORDER SUMMARY ---")
print(f"Cart Total:       ₹{cart_value:.2f}")

if coupon_applied:
    print(f"Coupon ('{VALID_COUPON}'): -₹{discount_amount:.2f} (50% OFF)")
else:
    print("Coupon Applied:   None / Invalid Code")

print("-" * 22)
print(f"Net Payable:      ₹{net_payable:.2f}")
