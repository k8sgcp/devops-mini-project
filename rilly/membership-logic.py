from dataclasses import dataclass
from typing import Optional

# Define club thresholds (sorted highest to lowest for clean evaluation)
TIER_THRESHOLDS = [
    ("Platinum", 885_000),
    ("Gold", 575_000),
    ("Silver", 300_000),
]

def determine_club(total_steps: int) -> Optional[str]:
    """
    Returns the highest eligible club tier for a given total step count.
    Returns None if the user hasn't met the minimum threshold.
    """
    for tier_name, threshold in TIER_THRESHOLDS:
        if total_steps >= threshold:
            return tier_name
    return None

@dataclass
class User:
    user_id: str
    name: str
    total_steps: int = 0
    club: Optional[str] = None

    def add_steps(self, steps: int) -> Optional[str]:
        """
        Adds new activity steps and updates the user's club status.
        Returns the new tier name if a upgrade occurred, otherwise None.
        """
        if steps < 0:
            raise ValueError("Steps added must be positive.")

        self.total_steps += steps
        new_club = determine_club(self.total_steps)

        # Check if user earned a new/higher tier
        if new_club != self.club:
            old_club = self.club
            self.club = new_club
            return new_club  # Signals a tier update/upgrade event

        return None

# --- Example Usage ---
if __name__ == "__main__":
    user = User(user_id="usr_101", name="Alex")

    # Day 1: Log initial activity
    user.add_steps(250_000)
    print(f"{user.name} Steps: {user.total_steps:,} | Club: {user.club}")
    # Output: Alex Steps: 250,000 | Club: None

    # Day 2: Cross Silver threshold (300,000)
    upgraded_to = user.add_steps(60_000)
    if upgraded_to:
        print(f"🎉 Upgrade! {user.name} joined the {upgraded_to} Club!")
    print(f"{user.name} Steps: {user.total_steps:,} | Club: {user.club}")
    # Output: 🎉 Upgrade! Alex joined the Silver Club!

    # Day 3: Jump straight to Platinum (885,000+)
    upgraded_to = user.add_steps(600_000)
    if upgraded_to:
        print(f"🎉 Upgrade! {user.name} joined the {upgraded_to} Club!")
    print(f"{user.name} Steps: {user.total_steps:,} | Club: {user.club}")
    # Output: 🎉 Upgrade! Alex joined the Platinum Club!
