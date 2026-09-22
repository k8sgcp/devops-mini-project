from datetime import datetime, timedelta

def process_recurring_subscriptions(db, payment_gateway, order_system):
    """
    Runs daily (via cron or task scheduler) to process due orders.
    """
    today = datetime.now().date()

    # 1. Fetch active subscriptions due today or overdue
    due_subscriptions = db.query(
        "SELECT * FROM subscriptions WHERE status = 'ACTIVE' AND next_order_date <= ?",
        (today,)
    )

    for sub in due_subscriptions:
        customer_id = sub['customer_id']
        product_id = sub['product_id']
        amount = sub['product_price']

        # 2. Attempt wallet debit
        debit_success = payment_gateway.debit_wallet(customer_id, amount)

        if debit_success:
            # 3. Create the order
            order_system.create_order(customer_id, product_id)

            # 4. Advance next order date by 60 calendar days
            new_next_date = sub['next_order_date'] + timedelta(days=60)

            db.execute(
                "UPDATE subscriptions SET next_order_date = ? WHERE id = ?",
                (new_next_date, sub['id'])
            )
        else:
            # Handle payment failure (e.g., notify customer, retry logic)
            handle_failed_payment(sub['id'])



# End of file
# This code shall be built and tested in Github actions before being pushed to production
