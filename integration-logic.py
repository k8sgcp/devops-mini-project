pip install flask razorpay
import os
from flask import Flask, render_template_string, request, jsonify
import razorpay

app = Flask(__name__)

# Initialize Razorpay Client with your Test/Live API Keys
# Best practice: Load these from environment variables
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "your_key_id")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "your_key_secret")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# 1. Checkout Page Route
@app.route("/")
def index():
    # Simple embedded HTML for demonstration
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Checkout</title>
    </head>
    <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
        <h2>Simple Razorpay Checkout</h2>
        <p>Product: Premium Subscription - ₹500</p>
        <button id="pay-btn" style="padding: 10px 20px; background-color: #3399cc; color: white; border: none; border-radius: 4px; cursor: pointer;">
            Pay with Razorpay
        </button>

        <!-- Razorpay Checkout Script -->
        <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
        <script>
            document.getElementById('pay-btn').onclick = async function (e) {
                // Step A: Request Order ID from Backend
                const response = await fetch('/create-order', { method: 'POST' });
                const orderData = await response.json();

                // Step B: Configure Razorpay Checkout Options
                var options = {
                    "key": "{{ key_id }}",
                    "amount": orderData.amount, // Amount in currency subunits (e.g., paise)
                    "currency": "INR",
                    "name": "Your Company Name",
                    "description": "Test Transaction",
                    "order_id": orderData.id, // Order ID generated from backend
                    "handler": function (response){
                        alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
                        // Here you would typically send these details to /verify-payment
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                };

                var rzp1 = new Razorpay(options);
                rzp1.open();
                e.preventDefault();
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, key_id=RAZORPAY_KEY_ID)

# 2. Create Order API Route
@app.route("/create-order", methods=["POST"])
def create_order():
    # Amount is in the smallest currency unit (e.g., 50000 paise = ₹500)
    order_data = {
        "amount": 50000,
        "currency": "INR",
        "payment_capture": 1 # 1 = Automatic capture, 0 = Manual capture
    }

    try:
        order = client.order.create(data=order_data)
        return jsonify(order)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
