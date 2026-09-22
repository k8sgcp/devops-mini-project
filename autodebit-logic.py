from datetime import datetime, timedelta

class CustomerAccount:
    def __init__(self, customer_id: str, wallet_balance: float, plan_cost: float, plan_duration_days: int):
        self.customer_id = customer_id
        self.wallet_balance = wallet_balance
        self.plan_cost = plan_cost
        self.plan_duration_days = plan_duration_days
        self.auto_debit_enabled = True

        # Set initial plan expiry to right now for demonstration
        self.expiry_date = datetime.now()

    def process_auto_recharge(self) -> bool:
        """Checks validity and auto-debits if expired."""
        current_time = datetime.now()

        # Step 1: Check if plan is expired
        if current_time >= self.expiry_date:
            print(f"[{self.customer_id}] Plan expired on {self.expiry_date.strftime('%Y-%m-%d %H:%M:%S')}.")

            if not self.auto_debit_enabled:
                print(f"[{self.customer_id}] Auto-debit disabled. Recharge cancelled.")
                return False

            # Step 2: Check wallet balance
            if self.wallet_balance >= self.plan_cost:
                # Step 3: Deduct amount & extend validity
                self.wallet_balance -= self.plan_cost
                self.expiry_date = current_time + timedelta(days=self.plan_duration_days)

                print(f"[{self.customer_id}] Auto-debit successful! Deducted ₹{self.plan_cost}.")
                print(f"[{self.customer_id}] New Expiry: {self.expiry_date.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"[{self.customer_id}] Remaining Balance: ₹{self.wallet_balance}\n")
                return True
            else:
                print(f"[{self.customer_id}] Insufficient balance (₹{self.wallet_balance}). Auto-debit failed.\n")
                return False
        else:
            print(f"[{self.customer_id}] Plan active until {self.expiry_date.strftime('%Y-%m-%d %H:%M:%S')}.\n")
            return False


# --- Example Usage ---
if __name__ == "__main__":
    # Initialize customer with ₹500 balance, ₹299 plan, 28 days validity
    user = CustomerAccount(customer_id="CUST_101", wallet_balance=500.0, plan_cost=299.0, plan_duration_days=28)

    # Trigger the auto-recharge check
    user.process_auto_recharge()



# End of file
# This code will be auto tested via Github actions before it deloyed to production env
