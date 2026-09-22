from datetime import datetime, date, timedelta

COINS_PER_1000_STEPS = 10
BONUS_MILESTONE_STEPS = 250_000
BONUS_COINS = 500
CYCLE_DAYS = 30

# In-memory database representation
user_state = {
    "wallet_balance": 0,
    "daily_steps_log": {},       # Format: { date_object: total_steps }
    "bonus_claimed_cycles": []   # Tracks cycle start dates that already awarded bonus
}

def is_within_active_hours(timestamp: datetime) -> bool:
    """Checks if time is between 05:30 and 22:30."""
    start_time = timestamp.replace(hour=5, minute=30, second=0, microsecond=0).time()
    end_time = timestamp.replace(hour=22, minute=30, second=0, microsecond=0).time()
    return start_time <= timestamp.time() <= end_time


def calculate_30_day_total(log: dict, current_date: date) -> int:
    """Sum steps for the current 30-day window (current date and past 29 days)."""
    start_date = current_date - timedelta(days=CYCLE_DAYS - 1)
    return sum(steps for log_date, steps in log.items() if start_date <= log_date <= current_date)


def record_daily_steps_and_award_coins(user_data: dict, step_date: date, total_steps: int, current_time: datetime):
    """
    Main logic: Awards daily coins and checks for 30-day milestone bonus.
    """
    # 1. Active window validation
    if not is_within_active_hours(current_time):
        print(f"[{current_time.strftime('%H:%M')}] Sync ignored: Outside active hours (05:30 - 22:30).")
        return

    # 2. Daily reward calculation
    daily_coins = (total_steps // 1000) * COINS_PER_1000_STEPS
    user_data["daily_steps_log"][step_date] = total_steps
    user_data["wallet_balance"] += daily_coins

    print(f"Daily Sync ({step_date}): {total_steps} steps -> +{daily_coins} coins.")

    # 3. 30-Day Bonus Check
    rolling_total_steps = calculate_30_day_total(user_data["daily_steps_log"], step_date)

    # Calculate current 30-day window start marker to prevent duplicate payouts within the same window
    current_window_start = step_date - timedelta(days=CYCLE_DAYS - 1)

    if rolling_total_steps >= BONUS_MILESTONE_STEPS:
        if current_window_start not in user_data["bonus_claimed_cycles"]:
            user_data["wallet_balance"] += BONUS_COINS
            user_data["bonus_claimed_cycles"].append(current_window_start)
            print(f"🎉 MILESTONE REACHED! 30-day steps: {rolling_total_steps:,} / {BONUS_MILESTONE_STEPS:,}. Bonus +{BONUS_COINS} coins added!")
        else:
            print(f"Milestone step count met ({rolling_total_steps:,}), but bonus was already claimed for this cycle.")

    print(f"Current Total Wallet Balance: {user_data['wallet_balance']} coins\n")


# --- Demonstration ---
today = date.today()
now = datetime.now().replace(hour=10, minute=0) # 10:00 AM (Active time)

# Simulate past 29 days with 8,500 steps/day (8,500 * 29 = 246,500 steps)
for i in range(29, 0, -1):
    past_date = today - timedelta(days=i)
    user_state["daily_steps_log"][past_date] = 8500
    user_state["wallet_balance"] += (8500 // 1000) * COINS_PER_1000_STEPS

# Day 30 sync: Adding 4,000 steps brings rolling total to 250,500 steps
print("--- Day 30 Sync ---")
record_daily_steps_and_award_coins(user_state, today, 4000, now)
