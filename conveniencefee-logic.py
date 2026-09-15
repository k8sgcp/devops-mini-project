from datetime import datetime, time

class Checkout:
    BASE_PLATFORM_FEE = 25
    LATE_NIGHT_FEE = 50

    @staticmethod
    def is_late_night_order(order_time: datetime = None) -> bool:
        """
        Checks if an order falls between 11:00 PM (23:00) and 3:00 AM (03:00).
        """
        current_time = (order_time or datetime.now()).time()
        
        # Late night window: 23:00 to 23:59:59 OR 00:00:00 to 03:00
        start_time = time(23, 0)  # 11:00 PM
        end_time = time(3, 0)     # 3:00 AM

        return current_time >= start_time or current_time < end_time

    @classmethod
    def calculate_order_total(cls, items_total: float, order_time: datetime = None) -> dict:
        """
        Calculates total payable amount including platform fee and convenience fee.
        """
        is_late_night = cls.is_late_night_order(order_time)
        convenience_fee = cls.LATE_NIGHT_FEE if is_late_night else 0
        
        total_payable = items_total + cls.BASE_PLATFORM_FEE + convenience_fee

        return {
            "items_total": items_total,
            "platform_fee": cls.BASE_PLATFORM_FEE,
            "convenience_fee": convenience_fee,
            "is_late_night": is_late_night,
            "total_payable": total_payable
        }


# --- Usage Examples ---

# Case 1: Order placed at 11:30 PM (Triggers ₹50 fee)
late_order_time = datetime(2026, 9, 15, 23, 30)
bill_1 = Checkout.calculate_order_total(items_total=1200.00, order_time=late_order_time)
print("--- 11:30 PM Order ---")
print(f"Convenience Fee: ₹{bill_1['convenience_fee']}")
print(f"Total Payable:   ₹{bill_1['total_payable']}")

# Case 2: Order placed at 2:15 AM (Triggers ₹50 fee)
early_morning_time = datetime(2026, 9, 16, 2, 15)
bill_2 = Checkout.calculate_order_total(items_total=1200.00, order_time=early_morning_time)
print("\n--- 2:15 AM Order ---")
print(f"Convenience Fee: ₹{bill_2['convenience_fee']}")
print(f"Total Payable:   ₹{bill_2['total_payable']}")

# Case 3: Order placed at 4:00 PM (No convenience fee)
regular_time = datetime(2026, 9, 15, 16, 0)
bill_3 = Checkout.calculate_order_total(items_total=1200.00, order_time=regular_time)
print("\n--- 4:00 PM Order ---")
print(f"Convenience Fee: ₹{bill_3['convenience_fee']}")
print(f"Total Payable:   ₹{bill_3['total_payable']}")
