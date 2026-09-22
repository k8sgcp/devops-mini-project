import firebase_admin
from firebase_admin import credentials, messaging

# 1. Initialize Firebase Admin SDK (run once at startup)
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def send_order_shipped_notification(user_fcm_token: str, order_id: str):
    """Sends a push notification to a user's device when their order is shipped."""

    # Construct the push notification payload
    message = messaging.Message(
        notification=messaging.Notification(
            title="Order Shipped! 📦",
            body=f"Great news! Your order #{order_id} has been shipped and is on its way.",
        ),
        data={
            "order_id": str(order_id),
            "event_type": "ORDER_SHIPPED",
            "click_action": "OPEN_ORDER_DETAILS",
        },
        token=user_fcm_token,  # Target device's unique FCM token
    )

    try:
        # Send the message
        response = messaging.send(message)
        print(f"Successfully sent notification for Order #{order_id}. Response ID: {response}")
        return True
    except Exception as e:
        print(f"Failed to send notification for Order #{order_id}: {e}")
        return False


def handle_order_status_update(order_id: str, new_status: str, user_fcm_token: str):
    """Business logic entry point when an order status changes."""

    if new_status.lower() == "shipped":
        send_order_shipped_notification(
            user_fcm_token=user_fcm_token,
            order_id=order_id
        )


# --- Example Usage ---
if __name__ == "__main__":
    # Retrieved from your database for the user/order
    sample_fcm_token = "user_device_fcm_token_here"
    sample_order_id = "ORD-98765"

    # Simulate an order shipping event
    handle_order_status_update(
        order_id=sample_order_id,
        new_status="shipped",
        user_fcm_token=sample_fcm_token
    )

# End of file
