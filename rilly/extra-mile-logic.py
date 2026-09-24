def check_smartwatch_eligibility(daily_step_logs, month_days=30):
    """
    Evaluates eligibility for an 80% smartwatch discount coupon.
    
    :param daily_step_logs: List or dict of daily step counts (calculated on a strict 24-hr cycle)
    :param month_days: Total days in the month being evaluated (default: 30)
    :return: dict with eligibility status and coupon details
    """
    # Count days where daily step count exceeds 10,000
    qualifying_days = sum(1 for steps in daily_step_logs if steps > 10000)
    
    is_eligible = qualifying_days > 25
    
    if is_eligible:
        return {
            "eligible": True,
            "qualifying_days": qualifying_days,
            "discount_percent": 80,
            "coupon_code": "SMARTWATCH80",
            "message": f"Congratulations! You completed >10k steps on {qualifying_days} days. Here is your 80% off coupon!"
        }
    
    return {
        "eligible": False,
        "qualifying_days": qualifying_days,
        "discount_percent": 0,
        "coupon_code": None,
        "message": f"You completed >10k steps on {qualifying_days} days. You need strictly more than 25 days to qualify."
    }


# Example Usage:
if __name__ == "__main__":
    # Simulated 30-day step counts for a user
    user_steps = [
        12000, 11000, 10500, 13000, 14000, 11500, 10200, 10800, 12500, 11100,
        10900, 13200, 14100, 10400, 12200, 10700, 11800, 10300, 12900, 11400,
        10600, 13500, 12100, 10100, 11000, 12800, 9500, 8000, 7500, 9000
    ]

    result = check_smartwatch_eligibility(user_steps)
    print(result)
