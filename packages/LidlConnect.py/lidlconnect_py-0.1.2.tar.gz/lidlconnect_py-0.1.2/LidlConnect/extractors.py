"""HTML and data extraction for Lidl Connect API."""

from bs4 import BeautifulSoup
import re
from typing import Tuple

class ExtractorMixin:
    """HTML extraction methods for Lidl Connect API."""
    
    def _get_soup(self, url: str) -> BeautifulSoup:
        """Get BeautifulSoup object from URL."""
        r = self.session.get(url)
        return BeautifulSoup(r.text, "html.parser")
    
    def _extract_csrf(self, soup: BeautifulSoup) -> str:
        """Extract CSRF token from dashboard HTML."""
        meta = soup.find("meta", {"name": "csrf-token"})
        if not meta or not meta.get("content"):
            raise ValueError("CSRF token not found in dashboard HTML")
        return meta["content"]
    
    def _extract_user_and_endpoint(self, soup: BeautifulSoup) -> Tuple[int, int]:
        """Extract user ID and endpoint ID from dashboard HTML."""
        all_scripts = ""
        for script in soup.find_all("script"):
            if script.string:
                all_scripts += script.string

        user_match = re.search(r"window\.user\s*=\s*\{.*?'user':\s*\{\s*\"id\":\s*(\d+).*?\"userType\":\s*\"CUSTOMER\"", all_scripts, re.DOTALL)
        endpoint_match = re.search(r'"endpoints":\s*\[\{\s*"id":\s*(\d+)', all_scripts, re.DOTALL)
        
        if not user_match or not endpoint_match:
            user_match = re.search(r'"id":\s*(\d+).*?"userType":\s*"CUSTOMER"', all_scripts, re.DOTALL)
            endpoint_match = re.search(r'"endpoints":\s*\[\{\s*"id":\s*(\d+)', all_scripts, re.DOTALL)
            
            if not user_match or not endpoint_match:
                raise ValueError("Could not extract userId or endpointId from scripts")
        
        return int(user_match.group(1)), int(endpoint_match.group(1))