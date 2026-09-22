import random
import time
from datetime import datetime, timedelta

# Mock Database & Cache (In production, use Redis or Postgres/MongoDB)
BOOKINGS_DB = {
    "booking_123": {
        "customer_mobile": "+919876543210",
        "status": "TECHNICIAN_EN_ROUTE"
    }
}
OTP_CACHE = {}  # Format: {booking_id: {"otp": "1234", "expires_at": timestamp}}

def generate_otp(length=4) -> str:
    """Generate a random numeric OTP."""
    return "".join([str(random.randint(0, 9)) for _ in range(length)])

def send_sms(mobile: str, otp: str):
    """Integrate your SMS gateway here (e.g., Twilio, MSG91, Fast2SMS)."""
    print(f"[SMS Gateway] Sent OTP {otp} to {mobile}")

def on_technician_arrived(booking_id: str) -> dict:
    """Triggered when technician clicks 'Arrived' in app."""
    booking = BOOKINGS_DB.get(booking_id)
    if not booking:
        return {"status": "error", "message": "Booking not found"}

    # 1. Generate 4-digit OTP & expiration (10 mins)
    otp = generate_otp(4)
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    # 2. Store in cache
    OTP_CACHE[booking_id] = {
        "otp": otp,
        "expires_at": expires_at,
        "attempts": 0
    }

    # 3. Update status & send SMS to customer
    booking["status"] = "ARRIVED_AWAITING_OTP"
    send_sms(booking["customer_mobile"], otp)

    return {"status": "success", "message": "OTP sent to customer"}

def verify_arrival_otp(booking_id: str, input_otp: str) -> dict:
    """Triggered when technician submits customer's OTP."""
    cached_data = OTP_CACHE.get(booking_id)
    booking = BOOKINGS_DB.get(booking_id)

    if not cached_data or not booking:
        return {"status": "error", "message": "Invalid session"}

    # Check expiration
    if datetime.utcnow() > cached_data["expires_at"]:
        return {"status": "error", "message": "OTP expired"}

    # Check attempt count to prevent brute force
    if cached_data["attempts"] >= 3:
        return {"status": "error", "message": "Too many failed attempts"}

    # Verify OTP
    if cached_data["otp"] == input_otp:
        booking["status"] = "IN_PROGRESS"
        del OTP_CACHE[booking_id]  # Clear used OTP
        return {"status": "success", "message": "Arrival verified. Job started!"}
    else:
        cached_data["attempts"] += 1
        return {"status": "error", "message": "Incorrect OTP"}

# Example Usage
if __name__ == "__main__":
    # 1. Technician taps "Arrived"
    print(on_technician_arrived("booking_123"))

    # 2. Technician enters correct OTP from customer
    customer_otp = OTP_CACHE["booking_123"]["otp"]
    print(verify_arrival_otp("booking_123", customer_otp))



# End of file
