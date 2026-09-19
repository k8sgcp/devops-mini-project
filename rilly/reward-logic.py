def calculate_coins(steps: int) -> int:
    """
    Calculates coins earned based on total daily steps.
    Rule: 10 coins for every completed 1,000 steps.
    """
    COINS_PER_INTERVAL = 10
    STEP_INTERVAL = 1000
    
    # Integer division ensures reward is given only for every FULL 1,000 steps
    return (steps // STEP_INTERVAL) * COINS_PER_INTERVAL


def process_daily_reward(user_id: str, steps: int, current_time_str: str, wallet: dict) -> dict:
    """
    Awards coins to the user's wallet if steps fall within active hours (05:30 to 22:30).
    """
    ACTIVE_START = "05:30"
    ACTIVE_END = "22:30"
    
    # Check if the event/sync is within active hours
    if not (ACTIVE_START <= current_time_str <= ACTIVE_END):
        print(f"[{current_time_str}] Outside active tracking window (05:30 - 22:30). Steps ignored.")
        return wallet
    
    earned_coins = calculate_coins(steps)
    
    # Add to existing balance or initialize if new
    wallet[user_id] = wallet.get(user_id, 0) + earned_coins
    
    print(f"[{current_time_str}] User {user_id}: {steps} steps -> +{earned_coins} coins earned. New Balance: {wallet[user_id]}")
    return wallet


# --- Example Usage ---
user_wallet = {}

# Test 1: Active hours with 4,750 steps (4 full 1,000s = 40 coins)
process_daily_reward(user_id="user_01", steps=4750, current_time_str="08:15", wallet=user_wallet)

# Test 2: Outside active hours (e.g., 11:00 PM)
process_daily_reward(user_id="user_01", steps=1200, current_time_str="23:00", wallet=user_wallet)

# Test 3: Active hours with 2,100 steps (+20 coins)
process_daily_reward(user_id="user_01", steps=2100, current_time_str="19:45", wallet=user_wallet)
