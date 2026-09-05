import os
import requests
from typing import Dict, Any, Optional

class BNPLPaymentLinker:
    def __init__(self, provider_name: str, api_key: str):
        self.provider = provider_name.lower()
        self.api_key = api_key
        # Example API endpoints (Mocked - actual URLs provided by PayU/Amazon Payment gateways)
        self.base_url = f"https://api.gateway.com/v1/{self.provider}"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def check_eligibility(self, phone_number: str) -> Dict[str, Any]:
        """Check if the user's mobile number is eligible for BNPL."""
        payload = {"phone_number": phone_number}
        try:
            # Simulate API call to BNPL gateway (e.g., LazyPay/Amazon Pay API)
            response = requests.post(
                f"{self.base_url}/check-eligibility", 
                json=payload, 
                headers=self._get_headers(),
                timeout=5
            )
            # Example response handling
            if response.status_code == 200:
                return response.json() # Returns {'eligible': True, 'credit_limit': 5000}
            return {"eligible": False, "reason": "Account not found or ineligible"}
        except requests.RequestException as e:
            return {"eligible": False, "error": str(e)}

    def initiate_linking_otp(self, phone_number: str, zepto_user_id: str) -> Dict[str, Any]:
        """Trigger an OTP to the user's mobile number to bind the BNPL account."""
        payload = {
            "phone_number": phone_number,
            "merchant_user_id": zepto_user_id
        }
        response = requests.post(
            f"{self.base_url}/link/send-otp", 
            json=payload, 
            headers=self._get_headers()
        )
        return response.json() # Returns {'reference_id': 'txn_123', 'status': 'OTP_SENT'}

    def verify_otp_and_link(self, reference_id: str, otp: str) -> Dict[str, Any]:
        """Verify OTP and return a payment token to store in Zepto DB."""
        payload = {
            "reference_id": reference_id,
            "otp": otp
        }
        response = requests.post(
            f"{self.base_url}/link/verify-otp", 
            json=payload, 
            headers=self._get_headers()
        )
        return response.json() # Returns {'status': 'SUCCESS', 'bnpl_token': 'tok_xyz123'}


# --- Example Integration Workflow ---
def handle_user_payment_linking(user_phone: str, zepto_user_id: str, provider: str) -> Optional[str]:
    linker = BNPLPaymentLinker(provider_name=provider, api_key="YOUR_PAYMENT_GATEWAY_KEY")
    
    # Step 1: Check if eligible
    eligibility = linker.check_eligibility(user_phone)
    if not eligibility.get("eligible"):
        print(f"{provider.capitalize()} is not available for this phone number.")
        return None

    print(f"User is eligible! Available Credit: ₹{eligibility.get('credit_limit', 0)}")
    
    # Step 2: Request OTP for Linking
    otp_res = linker.initiate_linking_otp(user_phone, zepto_user_id)
    ref_id = otp_res.get("reference_id")
    
    # Step 3: Verify OTP (Simulating user input)
    user_entered_otp = "123456" 
    verification = linker.verify_otp_and_link(ref_id, user_entered_otp)
    
    if verification.get("status") == "SUCCESS":
        bnpl_token = verification.get("bnpl_token")
        # Save `bnpl_token` into Zepto DB under the user's saved payment methods
        return bnpl_token
    
    return None
