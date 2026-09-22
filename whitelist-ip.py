import urllib.request
import json

def is_request_from_india(client_ip: str) -> bool:
    """
    Checks if a given IP address originates from India ('IN').
    Uses ip-api.com (free, rate-limited to 45 requests/min).
    """
    url = f"http://ip-api.com/json/{client_ip}?fields=status,countryCode"

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode('utf-8'))

            if data.get("status") == "success":
                return data.get("countryCode") == "IN"
    except Exception as e:
        print(f"Geolocation lookup failed: {e}")

    return False

# Example Usage:
client_ip = "103.217.220.1"  # Example Indian IP

if is_request_from_india(client_ip):
    print("Access Granted: Welcome to the site!")
else:
    print("Access Denied: This website is only accessible within India.")

# End of file
# Build and test shall be executed via Github Actions workflow
