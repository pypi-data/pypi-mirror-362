"""Usage-related API functionality for Lidl Connect."""

from typing import Dict, Any, Optional
from ..helpers import ttl_cache

class UsageMixin:
    """Usage-related API methods for Lidl Connect."""
    
    USAGE_URL = "https://selfcare.lidl-connect.at/customer/usage/"
    
    @ttl_cache(5)
    def get_usage_data(self) -> Dict[str, Any]:
        """
        Get usage data for the current account.
        
        Returns:
            Dict: Usage data including instanceGroups with counters
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
        
        r = self.session.post(self.USAGE_URL, headers=headers, json=payload)
        if r.status_code != 200:
            raise ValueError(f"Usage request failed: {r.status_code} {r.text!r}")
        
        return r.json()
    
    def print_usage_summary(self, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Pretty-print usage summary data.
        
        Args:
            data: Optional usage data. If None, will fetch new data
        """
        if data is None:
            data = self.get_usage_data()
        
        for group in data.get("instanceGroups", []):
            print(f"{group['itemName']} ({group['itemCategory']})")
            for elem in group.get("instanceElements", []):
                print(f"  • Valid: {elem['validFrom']} → {elem['validTo']}")
                for counter in elem.get("counters", []):
                    nv = counter["niceValue"]
                    unit = nv.get("type") or counter.get("baseValue", {}).get("type", "")
                    print(f"    - {counter['counterId']}: {nv['value']} / {nv['initialValue']} {unit}")
            print()
    
    def get_remaining_data(self) -> Dict[str, float]:
        """
        Get remaining data balance (in GiB).
        
        Returns:
            Dict with remaining, total, and used data in GiB
        """
        data = self.get_usage_data()
        result = {"remaining": 0, "total": 0, "used": 0}
        
        for group in data.get("instanceGroups", []):
            for elem in group.get("instanceElements", []):
                for counter in elem.get("counters", []):
                    if counter["counterId"] == "DATA":
                        nv = counter["niceValue"]
                        if nv.get("type") == "GiB":
                            result["remaining"] = nv["value"]
                            result["total"] = nv["initialValue"]
                            result["used"] = nv["initialValue"] - nv["value"]
        
        return result
    
    def get_remaining_eu_data(self) -> Dict[str, float]:
        """
        Get remaining EU data balance (in GiB).
        
        Returns:
            Dict with remaining, total, and used EU data in GiB
        """
        data = self.get_usage_data()
        result = {"remaining": 0, "total": 0, "used": 0}
        
        for group in data.get("instanceGroups", []):
            for elem in group.get("instanceElements", []):
                for counter in elem.get("counters", []):
                    if counter["counterId"] == "DATA_EU":
                        nv = counter["niceValue"]
                        if nv.get("type") == "GiB":
                            result["remaining"] = nv["value"]
                            result["total"] = nv["initialValue"]
                            result["used"] = nv["initialValue"] - nv["value"]
        
        return result
    
    def get_remaining_minutes(self) -> Dict[str, float]:
        """
        Get remaining voice minutes.
        
        Returns:
            Dict with remaining, total, and used minutes
        """
        data = self.get_usage_data()
        result = {"remaining": 0, "total": 0, "used": 0}
        
        for group in data.get("instanceGroups", []):
            for elem in group.get("instanceElements", []):
                for counter in elem.get("counters", []):
                    if counter["counterId"] == "VOICE_SMS":
                        nv = counter["niceValue"]
                        if nv.get("type") == "MIN":
                            result["remaining"] = nv["value"]
                            result["total"] = nv["initialValue"]
                            result["used"] = nv["initialValue"] - nv["value"]
        
        return result
    
    @property
    def tariff_package_valid_from(self) -> Optional[str]:
        """
        Get the start date of the current tariff package.
        
        Returns:
            ISO formatted date string or None if not available
        """
        try:
            data = self.get_usage_data()
            for group in data.get("instanceGroups", []):
                if group.get("itemCategory") == "TARIFF_PACKAGE":
                    for elem in group.get("instanceElements", []):
                        return elem.get("validFrom")
            return None
        except Exception:
            return None
    
    @property
    def tariff_package_valid_to(self) -> Optional[str]:
        """
        Get the end date of the current tariff package.
        
        Returns:
            ISO formatted date string or None if not available
        """
        try:
            data = self.get_usage_data()
            for group in data.get("instanceGroups", []):
                if group.get("itemCategory") == "TARIFF_PACKAGE":
                    for elem in group.get("instanceElements", []):
                        return elem.get("validTo")
            return None
        except Exception:
            return None
    
    @property
    def tariff_package_details(self) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about the current tariff package.
        
        Returns:
            Dict containing name, category, validFrom, validTo and other details
            or None if not available
        """
        try:
            data = self.get_usage_data()
            for group in data.get("instanceGroups", []):
                if group.get("itemCategory") == "TARIFF_PACKAGE":
                    result = {
                        "name": group.get("itemName"),
                        "category": group.get("itemCategory"),
                    }
                    
                    if group.get("instanceElements") and len(group.get("instanceElements")) > 0:
                        elem = group.get("instanceElements")[0]
                        result.update({
                            "validFrom": elem.get("validFrom"),
                            "validTo": elem.get("validTo"),
                            "counters": [
                                {
                                    "id": counter.get("counterId"),
                                    "value": counter.get("niceValue", {}).get("value"),
                                    "initialValue": counter.get("niceValue", {}).get("initialValue"),
                                    "unit": counter.get("niceValue", {}).get("type")
                                }
                                for counter in elem.get("counters", [])
                            ]
                        })
                    return result
            return None
        except Exception:
            return None