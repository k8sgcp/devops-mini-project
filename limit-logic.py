import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CosmicStorage")

class CosmicStorageAlert:
    def __init__(self, alert_threshold: float = 0.90):
        self.alert_threshold = alert_threshold

    def check_storage_status(self, bytes_used: int, total_bytes: int) -> dict:
        """
        Calculates storage usage percentage and triggers an alert
        if usage meets or exceeds the threshold.
        """
        if total_bytes <= 0:
            raise ValueError("Total bytes must be greater than 0.")

        usage_ratio = bytes_used / total_bytes
        usage_percentage = round(usage_ratio * 100, 2)

        is_alert_triggered = usage_ratio >= self.alert_threshold

        status = {
            "bytes_used": bytes_used,
            "total_bytes": total_bytes,
            "usage_percentage": usage_percentage,
            "alert_triggered": is_alert_triggered
        }

        if is_alert_triggered:
            self._send_alert(usage_percentage)

        return status

    def _send_alert(self, usage_percentage: float):
        """Triggers the notification logic (email, Slack, SMS, etc.)."""
        message = (
            f"⚠️ WARNING: Your Cosmic cloud storage is {usage_percentage}% full! "
            f"Please upgrade your plan or clear space to prevent upload blocks."
        )
        logger.warning(message)
        # Add notification integration here (e.g., requests.post(webhook_url, json={"text": message}))

# Example Usage
if __name__ == "__main__":
    monitor = CosmicStorageAlert(alert_threshold=0.90)

    # Example 1: Under limit (85GB of 100GB)
    monitor.check_storage_status(bytes_used=85 * (1024**3), total_bytes=100 * (1024**3))

    # Example 2: At or over limit (92GB of 100GB) -> Triggers Alert
    monitor.check_storage_status(bytes_used=92 * (1024**3), total_bytes=100 * (1024**3))
