"""Authentication-related functionality for Lidl Connect."""

from typing import Dict

class AuthMixin:
    """Authentication methods for Lidl Connect API."""
    
    LOGIN_PUK_URL = "https://selfcare.lidl-connect.at/de/customer/login/puk"
    LOGIN_PASSWORD_URL = "https://selfcare.lidl-connect.at/de/customer/login/account"
    LOGOUT_URL = "https://selfcare.lidl-connect.at/de/customer/logout"
    
    @property
    def login_url(self):
        """Get the appropriate login URL based on credentials."""
        return self.LOGIN_PUK_URL if self.puk else self.LOGIN_PASSWORD_URL
    
    def login(self) -> bool:
        """
        Log in to Lidl Connect.
        
        Returns:
            bool: True if login successful
        """
        login_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=utf-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://selfcare.lidl-connect.at",
            "Referer": "https://selfcare.lidl-connect.at/en/customer/login",
            "X-AUTH-SELF-CARE": "1",
            "locale": "en",
        }
        login_payload = {"identifier": self.identifier, "token": self.token}
        
        r = self.session.post(self.login_url, headers=login_headers, json=login_payload)
        if r.status_code != 200:
            return False
        
        self.logged_in = True
        return True
    
    def logout(self) -> bool:
        """
        Log out from Lidl Connect.
        
        Returns:
            bool: True if logout successful, False otherwise
        """
        if not self.logged_in:
            return True
            
        r = self.session.get(self.LOGOUT_URL)
        if r.status_code == 200 or r.status_code == 302:
            self.logged_in = False
            return True
        return False