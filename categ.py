from datetime import date


def get_age_tier(dob: date) -> str:
    """Calculates age from DOB and returns the age tier."""
    today = date.today()

    # Calculate exact age accounting for month/day
    age = (
        today.year
        - dob.year
        - ((today.month, today.day) < (dob.month, dob.day))
    )

    # Classify into tiers
    if age <= 25:
        return "ad"
    elif age <= 40:
        return "mi"
    elif age <= 60:
        return "se"
    else:
        return "sc"


# Example Usage:
user_dob = date(1995, 8, 15)  # Replace with actual DOB (YYYY, MM, DD)
tier = get_age_tier(user_dob)
print(f"Tier: {tier}")
