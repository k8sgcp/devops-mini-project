def calculate_avg_monthly_data(total_gb, days_in_cycle, cycle_days=30):
    if days_in_cycle <= 0:
        raise ValueError("Days in cycle must be greater than zero.")

    avg_daily_gb = total_gb / days_in_cycle
    avg_monthly_gb = avg_daily_gb * cycle_days

    return round(avg_daily_gb, 2), round(avg_monthly_gb, 2)

# Example usage: 150 GB used over 20 days
daily, monthly = calculate_avg_monthly_data(total_gb=150, days_in_cycle=20)
print(f"Daily Average: {daily} GB/day")
print(f"Projected Monthly Average (30 days): {monthly} GB/month")

# End of logic
