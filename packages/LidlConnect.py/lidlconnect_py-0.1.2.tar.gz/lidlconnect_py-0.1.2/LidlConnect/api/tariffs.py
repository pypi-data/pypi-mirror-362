"""Tariffs-related API functionality for Lidl Connect."""

from typing import Dict, Any, List
from ..helpers import ttl_cache

class TariffsMixin:
    """Tariffs-related API methods for Lidl Connect API."""
    
    TARIFFS_URL = "https://selfcare.lidl-connect.at/customer/tariffs/all-packages"
    
    @ttl_cache(60)
    def get_tariffs(self) -> List[Dict[str, Any]]:
        """
        Get all available tariffs for the current account.
        
        Returns:
            List[Dict]: List of tariff objects with relevant information
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
        r = self.session.post(self.TARIFFS_URL, headers=headers, json=payload)
        
        if r.status_code != 200:
            raise ValueError(f"Tariffs request failed: {r.status_code} {r.text!r}")
        
        data = r.json()
        tariffs = [item for item in data if item.get("category") == "TARIFF"]
        
        result = []
        for tariff in tariffs:
            processed_tariff = {
                "id": tariff.get("id"),
                "itemId": tariff.get("itemId"),
                "name": tariff.get("name"),
                "description": tariff.get("description"),
                "sort": tariff.get("sort", 0),
                "featured": tariff.get("featured", False),
                "visible": tariff.get("visible", True),
            }
            
            translations = tariff.get("translations")
            if translations and isinstance(translations, dict):
                german_translation = translations.get("de", {})
                if german_translation and isinstance(german_translation, dict):
                    processed_tariff["german_name"] = german_translation.get("name")
                    processed_tariff["german_content"] = german_translation.get("content")
                    processed_tariff["german_teaser"] = german_translation.get("teaser")
            
            result.append(processed_tariff)
        
        result.sort(key=lambda x: x.get("sort", 0))
        return result
    
    def print_tariffs(self) -> None:
        """
        Pretty-print available tariffs.
        """
        try:
            tariffs = self.get_tariffs()
            
            if not tariffs:
                print("\nNo tariff information available")
                return
                
            print(f"\n{'=' * 20} AVAILABLE TARIFFS {'=' * 20}")
            for tariff in tariffs:
                print(f"\n{'-' * 60}")
                print(f"Name: {tariff.get('german_name') or tariff.get('name')}")
                print(f"ID: {tariff.get('itemId')}")
                
                if tariff.get('german_teaser'):
                    import html
                    import re
                    
                    # HTML entities
                    teaser = html.unescape(tariff.get('german_teaser'))
                    
                    # style attributes
                    teaser = re.sub(r'style="[^"]*"', '', teaser)
                    teaser = re.sub(r'class="[^"]*"', '', teaser)
                    
                    # table structure
                    teaser = re.sub(r'<tr[^>]*>', '\n', teaser)
                    teaser = re.sub(r'<td[^>]*>', ' | ', teaser)
                    teaser = re.sub(r'</tr>', '', teaser)
                    teaser = re.sub(r'</td>', '', teaser)
                    
                    # line breaks
                    teaser = teaser.replace('<br>', '\n').replace('<br/>', '\n')
                    teaser = teaser.replace('<p>', '').replace('</p>', '\n')
                    
                    # divs and spans
                    teaser = re.sub(r'<div[^>]*>', '', teaser)
                    teaser = re.sub(r'</div>', '', teaser)
                    teaser = re.sub(r'<span[^>]*>', '', teaser)
                    teaser = re.sub(r'</span>', '', teaser)
                    
                    # other HTML tags
                    teaser = re.sub(r'<[^>]+>', '', teaser)
                    
                    # whitespace and cleanup
                    teaser = re.sub(r'\s+', ' ', teaser)
                    teaser = re.sub(r' \| ', ' | ', teaser)
                    teaser = re.sub(r'\n\s+', '\n', teaser)
                    
                    # newlines
                    teaser = re.sub(r'\n+', '\n', teaser)
                    
                    # special chars
                    teaser = teaser.replace('\\u00a0', ' ')
                    
                    # keep only printable ASCII chars
                    teaser = ''.join([i if ord(i) < 128 else ' ' for i in teaser])
                    
                    # other table tags
                    for tag in ['<table>', '</table>', '<tbody>', '</tbody>']:
                        teaser = teaser.replace(tag, '')
                    
                    print(f"\nDetails:\n{teaser.strip()}")
                
                print(f"Featured: {'✓' if tariff.get('featured') else '✗'}")
                print(f"Visible: {'✓' if tariff.get('visible') else '✗'}")
        except Exception as e:
            print(f"\nError fetching tariffs: {str(e)}")
            import traceback
            traceback.print_exc()