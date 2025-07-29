"""Credit-related API functionality for Lidl Connect."""

class CreditMixin:
    """Credit methods for Lidl Connect API."""
    
    CREDIT_URL = "https://selfcare.lidl-connect.at/credit/code"
    
    def credit_topup(self, code: str) -> bool:
        """
        Top up credit using a voucher code.
        
        Args:
            code: The voucher code to redeem
            
        Returns:
            True if the top up was successful, False otherwise.
        """
        if not self.logged_in or not self.csrf_token:
            raise ValueError("Not logged in or missing CSRF token")
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://selfcare.lidl-connect.at",
            "Referer": self.DASHBOARD_URL,
            "X-CSRF-TOKEN": self.csrf_token,
            "X-SELF-CARE": "1",
        }
        
        phone_number = self.phone_number
        if not phone_number:
            raise ValueError("Phone number not available")
        
        payload = {
            "phoneNumber": phone_number,
            "code": {
                "label": "credit_top_up.bon",
                "code_fields": 1,
                "code_field_length": 16,
                "code_validation": "^([a-zA-Z0-9]+)$",
                "active": True,
                "api_type": "VOUCHER_WITH_ACTIVATION_NUMBER",
                "code": code
            },
            "userId": self.user_id,
            "endpointId": self.endpoint_id
        }
        
        r = self.session.post(self.CREDIT_URL, headers=headers, json=payload)
        
        if r.status_code != 200:
            return False
        
        if hasattr(self._get_user_data, 'cache'):
            self._get_user_data.cache.clear()
        
        return True