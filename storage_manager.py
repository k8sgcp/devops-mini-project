import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CosmicStorage")

class CosmicStorageManager:
    # 100 GB expressed in bytes
    ADDITIONAL_STORAGE_BYTES = 100 * (1024**3)

    def __init__(self, alert_threshold: float = 0.90, auto_subscribe_enabled: bool = True):
        self.alert_threshold = alert_threshold
        self.auto_subscribe_enabled = auto_subscribe_enabled

    def process_storage_check(self, bytes_used: int, total_bytes: int) -> dict:
        """
        Monitors storage usage. If threshold is hit, sends an alert and
        triggers auto-subscription to expand quota by 100GB.
        """
        if total_bytes <= 0:
            raise ValueError("Total bytes must be greater than 0.")

        usage_ratio = bytes_used / total_bytes
        usage_percentage = round(usage_ratio * 100, 2)
        threshold_reached = usage_ratio >= self.alert_threshold

        status = {
            "bytes_used": bytes_used,
            "total_bytes": total_bytes,
            "usage_percentage": usage_percentage,
            "threshold_reached": threshold_reached,
            "auto_subscribed": False,
            "new_total_bytes": total_bytes
        }

        if threshold_reached:
            self._send_alert(usage_percentage)

            if self.auto_subscribe_enabled:
                new_total = self._trigger_auto_subscribe(total_bytes)
                status["auto_subscribed"] = True
                status["new_total_bytes"] = new_total

        return status

    def _send_alert(self, usage_percentage: float):
        """Triggers threshold notification."""
        logger.warning(
            f"⚠️ WARNING: Cosmic storage is at {usage_percentage}% capacity!"
        )

    def _trigger_auto_subscribe(self, current_total_bytes: int) -> int:
        """
        Executes auto-subscribe logic to purchase and provision
        100GB additional storage for Cosmic.
        """
        new_total_bytes = current_total_bytes + self.ADDITIONAL_STORAGE_BYTES

        logger.info("🔄 Auto-subscribe triggered: Submitting payment & provisioning 100GB...")

        # Mock API integration with Cosmic billing/provisioning service
        # e.g., cosmic_client.billing.add_addon_pack(pack_id="extra_100gb")

        logger.info(f"✅ Successfully expanded quota. New capacity: {new_total_bytes / (1024**3):.2f} GB")
        return new_total_bytes


# Example Usage
if __name__ == "__main__":
    # User has auto-subscribe turned ON
    manager = CosmicStorageManager(alert_threshold=0.90, auto_subscribe_enabled=True)

    # Example: 92GB used out of 100GB (92% capacity)
    initial_used = 92 * (1024**3)
    initial_total = 100 * (1024**3)

    result = manager.process_storage_check(bytes_used=initial_used, total_bytes=initial_total)
    print("\nCheck Summary:", result)
