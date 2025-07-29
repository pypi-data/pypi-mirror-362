"""Utility functionality for Lidl Connect API."""

from typing import Dict, Any, Union

class ApiMixin:
    """General API utilities for Lidl Connect."""
    
    def make_api_request(self, url: str, data: Dict = None, method: str = "POST") -> Union[Dict[str, Any], str]:
        """
        Make a generic API request to Lidl Connect.
        
        Args:
            url: API endpoint to call
            data: Payload to send (optional)
            method: HTTP method (default: POST)
            
        Returns:
            Dict or str: API response (JSON parsed if Content-Type is application/json)
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
        
        if method.upper() == "POST":
            r = self.session.post(url, headers=headers, json=data or {})
        else:
            r = self.session.get(url, headers=headers)
            
        if r.status_code >= 400:
            raise ValueError(f"API request failed: {r.status_code} {r.text!r}")
            
        return r.json() if r.headers.get('Content-Type') == 'application/json' else r.text