from datetime import date


def validate_account_creation(dob: date) -> bool:
    """Validates if user is at least 18 years old to create an account."""
    today = date.today()

    # Calculate exact age accounting for leap years and upcoming birthdays
    age = (
        today.year
        - dob.year
        - ((today.month, today.day) < (dob.month, dob.day))
    )

    if age < 18:
        raise ValueError(
            f"Account creation denied. User is {age} years old (minimum age required is 18)."
        )

    return True


# Example Usage:
try:
    user_dob = date(2010, 5, 20)  # Example DOB
    validate_account_creation(user_dob)
    print("Account created successfully.")
except ValueError as e:
    print(e)
