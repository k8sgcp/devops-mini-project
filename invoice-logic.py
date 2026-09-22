import datetime

def is_invoice_day(today=None):
    if today is None:
        today = datetime.date.today()

    # Send on the 30th of the month
    if today.day == 30:
        return True

    # Handle February (which has fewer than 30 days)
    if today.month == 2:
        next_day = today + datetime.timedelta(days=1)
        if next_day.month == 3:  # Last day of February
            return True

    return False

def send_invoice(customer_email, amount=399):
    # Replace this with your email sender (e.g., smtplib) or billing API
    print(f"Invoice of ₹{amount} sent to {customer_email}")

# Trigger this daily via Cron or Task Scheduler
if is_invoice_day():
    send_invoice("customer@example.com")


# End of file
