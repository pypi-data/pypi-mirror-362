"""User-related API functionality for Lidl Connect."""

from typing import Dict, Any, Optional
from ..helpers import ttl_cache

class UserDataMixin:
    """User data methods for Lidl Connect API."""
    
    USER_DATA_URL = "https://selfcare.lidl-connect.at/customer/dashboard/login-check"
    
    @ttl_cache(30)
    def _get_user_data(self) -> Dict[str, Any]:
        """
        Get user data from the server.
        
        Returns:
            Dict: User data including name, type, accounts, etc.
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
        
        payload = {"userId": self.user_id, "endpointId": self.endpoint_id}
        r = self.session.post(self.USER_DATA_URL, headers=headers, json=payload)
        
        if r.status_code != 200:
            raise ValueError(f"User data request failed: {r.status_code} {r.text!r}")
        
        return r.json()
    
    @property
    def user_name(self) -> Optional[str]:
        """Get user's name."""
        try:
            return self._get_user_data().get("name")
        except Exception:
            return None
        
    @property
    def phone_number(self) -> Optional[str]:
        """Get user's phonenumber."""
        try:
            data = self._get_user_data()
            if data and "accounts" in data and data["accounts"]:
                account = data["accounts"][0]
                if "endpoints" in account and account["endpoints"]:
                    endpoint = account["endpoints"][0]
                    return endpoint.get("name") # Phone number
            return None
        except Exception:
            return None
    
    @property
    def user_type(self) -> Optional[str]:
        """Get user's type (e.g., 'CUSTOMER')."""
        try:
            return self._get_user_data().get("userType")
        except Exception:
            return None
    
    @property
    def has_password(self) -> bool:
        """Check if user has set a password."""
        try:
            return self._get_user_data().get("hasPassword", False)
        except Exception:
            return False
    
    @property
    def birth_date(self) -> Optional[str]:
        """Get user's birth date."""
        try:
            return self._get_user_data().get("birthDate")
        except Exception:
            return None
    
    @property
    def status(self) -> Optional[str]:
        """Get endpoint status (e.g., 'ACTIVE')."""
        try:
            data = self._get_user_data()
            for account in data.get("accounts", []):
                for endpoint in account.get("endpoints", []):
                    if endpoint.get("id") == self.endpoint_id:
                        return endpoint.get("status")
            return None
        except Exception:
            return None
    
    @property
    def customer_type(self) -> Optional[str]:
        """Get customer type (e.g., 'ANONYM')."""
        try:
            return self._get_user_data().get("customerType")
        except Exception:
            return None
    
    @property
    def customer_language(self) -> Optional[str]:
        """Get customer language preference."""
        try:
            return self._get_user_data().get("customerLanguage")
        except Exception:
            return None
    
    @property
    def balance(self) -> Optional[float]:
        """Get account balance."""
        try:
            data = self._get_user_data()
            for account in data.get("accounts", []):
                for endpoint in account.get("endpoints", []):
                    if endpoint.get("id") == self.endpoint_id:
                        return endpoint.get("ocsBalance")
            return None
        except Exception:
            return None
            
    @property
    def activation_date(self) -> Optional[str]:
        """Get activation date."""
        try:
            data = self._get_user_data()
            for account in data.get("accounts", []):
                for endpoint in account.get("endpoints", []):
                    if endpoint.get("id") == self.endpoint_id:
                        return endpoint.get("activationDate")
            return None
        except Exception:
            return None
            
    @property
    def deactivation_date(self) -> Optional[str]:
        """Get deactivation date."""
        try:
            data = self._get_user_data()
            for account in data.get("accounts", []):
                for endpoint in account.get("endpoints", []):
                    if endpoint.get("id") == self.endpoint_id:
                        return endpoint.get("deactivationDate")
            return None
        except Exception:
            return None