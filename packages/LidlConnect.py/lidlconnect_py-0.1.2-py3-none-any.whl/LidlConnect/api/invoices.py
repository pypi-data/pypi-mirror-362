"""Invoices-related API functionality for Lidl Connect."""

from typing import Dict, Any, List, Optional
from datetime import datetime
from ..helpers import ttl_cache

class InvoicesMixin:
    """Invoices-related API methods for Lidl Connect API."""
    
    INVOICES_URL = "https://selfcare.lidl-connect.at/customer/invoices/invoice-list"
    VOUCHER_URL = "https://selfcare.lidl-connect.at/customer/invoices/consumed-vouchers"
    
    @ttl_cache(30)
    def get_invoices(self) -> List[Dict[str, Any]]:
        """
        Get list of invoices for the current account.
        
        Returns:
            List[Dict]: List of invoice objects with transaction details
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
            "ocrAvailable": "0",
        }
        
        payload = {"accountId": self.endpoint_id, "userId": self.user_id, "endpointId": self.endpoint_id}
        r = self.session.post(self.INVOICES_URL, headers=headers, json=payload)
        
        if r.status_code != 200:
            if r.status_code == 422 and r.text == '[]':
                return []
            raise ValueError(f"Invoices request failed: {r.status_code} {r.text!r}")
        
        return r.json()
    
    @ttl_cache(30)
    def get_vouchers(self) -> List[Dict[str, Any]]:
        """
        Get list of consumed vouchers for the current account.
        
        Returns:
            List[Dict]: List of voucher objects with transaction details
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
            "ocrAvailable": "0",
        }
        
        payload = {"userId": self.user_id, "endpointId": self.endpoint_id}
        r = self.session.post(self.VOUCHER_URL, headers=headers, json=payload)
        
        if r.status_code != 200:
            if r.status_code == 422 and r.text == '[]':
                return []
            raise ValueError(f"Vouchers request failed: {r.status_code} {r.text!r}")
        
        return r.json()
    
    def print_invoices(self) -> None:
        """
        Pretty-print invoice and voucher history.
        """
        try:
            invoices = self.get_invoices()
            vouchers = self.get_vouchers()
            
            if not invoices and not vouchers:
                print("\nNo payment history available")
                return
                
            if invoices:
                print(f"\n{'=' * 20} INVOICE HISTORY {'=' * 20}")
                
                for invoice in invoices:
                    try:
                        posting_date = datetime.fromisoformat(invoice.get("postingDate").replace("Z", "+00:00"))
                        date_str = posting_date.strftime("%d %b %Y, %H:%M")
                    except (ValueError, AttributeError):
                        date_str = invoice.get("postingDate", "Unknown date")
                    
                    payment_type = invoice.get("type", "").capitalize()
                    provider = invoice.get("provider", "")
                    channel = invoice.get("channel", "").replace("_", " ").title()
                    payment_method = f"{payment_type} via {provider} ({channel})"
                    
                    print(f"\n{'-' * 60}")
                    print(f"Transaction ID: {invoice.get('id')}")
                    print(f"Date: {date_str}")
                    print(f"Amount: €{invoice.get('amount', 0):.2f}")
                    print(f"Payment Method: {payment_method}")
            
            if vouchers:
                print(f"\n{'=' * 20} VOUCHER HISTORY {'=' * 20}")
                
                for voucher in vouchers:
                    try:
                        posting_date = datetime.fromisoformat(voucher.get("consumedDate").replace("Z", "+00:00"))
                        date_str = posting_date.strftime("%d %b %Y, %H:%M")
                    except (ValueError, AttributeError):
                        date_str = voucher.get("consumedDate", "Unknown date")
                    
                    print(f"\n{'-' * 60}")
                    print(f"Voucher ID: {voucher.get('id')}")
                    print(f"Serial: {voucher.get('serial')}")
                    print(f"Value: €{voucher.get('balanceAdvice', 0):.2f}")
                    print(f"Consumed Date: {date_str}")
        except Exception as e:
            print(f"\nError fetching payment history: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def get_total_spent(self) -> float:
        """
        Calculate the total amount spent across all invoices and vouchers.
        
        Returns:
            float: Total amount in euros
        """
        total = 0.0
        try:
            invoices = self.get_invoices()
            vouchers = self.get_vouchers()
            total += sum(invoice.get("amount", 0) for invoice in invoices)
            total += sum(voucher.get("balanceAdvice", 0) for voucher in vouchers)
        except Exception:
            pass
        return total
    
    @property
    def last_payment_date(self) -> Optional[str]:
        """
        Get the date of the most recent payment from either invoices or vouchers.
        
        Returns:
            str: ISO formatted date string or None if no payments
        """
        try:
            all_dates = []
            
            invoices = self.get_invoices()
            invoice_dates = [(invoice.get("postingDate"), invoice.get("amount")) 
                             for invoice in invoices if invoice.get("postingDate")]
            
            vouchers = self.get_vouchers()
            voucher_dates = [(voucher.get("consumedDate"), voucher.get("balanceAdvice")) 
                            for voucher in vouchers if voucher.get("consumedDate")]
            
            all_dates = invoice_dates + voucher_dates
            if not all_dates:
                return None
                
            all_dates.sort(key=lambda x: x[0], reverse=True)
            return all_dates[0][0]
        except Exception:
            return None