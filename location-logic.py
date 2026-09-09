import logging
from typing import Optional
from fastapi import FastAPI, Header, HTTPException, Request, status
from pydantic import BaseModel, EmailStr
import requests

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("account_verification")

app = FastAPI(title="Location-Based Account Creation API")

# Allowed ISO 3166-1 alpha-2 country codes
ALLOWED_COUNTRIES = {"US", "CA"}  # United States and Canada


# --- Data Models ---
class UserRegistrationRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class RegistrationResponse(BaseModel):
    status: str
    message: str
    detected_country: Optional[str] = None


# --- IP Geolocation Utility ---
def get_country_from_ip(ip_address: str) -> Optional[dict]:
    """Queries ipapi.co to determine the ISO country code for a given IP."""
    # Skip geolocation for local/loopback IPs during testing
    if ip_address in {"127.0.0.1", "localhost", "::1"}:
        logger.info("Loopback IP detected. Defaulting to US for local test.")
        return {"country_code": "US", "country_name": "United States (Local)"}

    try:
        url = f"https://ipapi.co/{ip_address}/json/"
        headers = {"User-Agent": "LocationChecker/1.0"}
        response = requests.get(url, headers=headers, timeout=3.0)

        if response.status_code == 200:
            data = response.json()
            return {
                "country_code": data.get("country_code"),
                "country_name": data.get("country_name"),
            }
        logger.warning(
            f"Geolocation API returned HTTP {response.status_code} for IP {ip_address}"
        )
        return None
    except requests.RequestException as err:
        logger.error(
            f"Geolocation request failed for IP {ip_address}: {str(err)}"
        )
        return None


def get_client_ip(
    request: Request, x_forwarded_for: Optional[str] = Header(None)
) -> str:
    """Extracts the true client IP address, handling proxy headers (e.g., NGINX, Cloudflare)."""
    if x_forwarded_for:
        # 'X-Forwarded-For' can be a comma-separated list; first entry is the real client IP
        return x_forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"


# --- API Endpoint ---
@app.post(
    "/api/v1/register",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserRegistrationRequest,
    request: Request,
    x_forwarded_for: Optional[str] = Header(None),
):
    """Handles user registration with strict geolocation checks."""
    client_ip = get_client_ip(request, x_forwarded_for)
    location_data = get_country_from_ip(client_ip)

    if not location_data or not location_data.get("country_code"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to verify location. Registration temporarily unavailable.",
        )

    country_code = location_data["country_code"]
    country_name = location_data["country_name"]

    # Restrict account creation if client is outside allowed regions
    if country_code not in ALLOWED_COUNTRIES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"Account creation is denied. Service is currently only available "
                f"in the US and Canada (Detected location: {country_name})."
            ),
        )

    # Proceed with account creation logic
    logger.info(
        f"User '{user_data.username}' registered successfully from IP {client_ip} ({country_name})."
    )

    return RegistrationResponse(
        status="success",
        message="Account created successfully.",
        detected_country=country_name,
    )


# --- Execution ---
if __name__ == "__main__":
    import uvicorn

    # Run local server on http://127.0.0.1:8000
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
