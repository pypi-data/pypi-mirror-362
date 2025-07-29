"""Main client class for Lidl Connect API."""

import requests
import signal
import atexit

from .auth import AuthMixin
from .extractors import ExtractorMixin
from .api.usage import UsageMixin
from .api.utils import ApiMixin
from .api.user import UserDataMixin
from .api.tariffs import TariffsMixin
from .api.invoices import InvoicesMixin
from .api.credit import CreditMixin

class LidlConnect(AuthMixin, ExtractorMixin, UsageMixin, ApiMixin, UserDataMixin, TariffsMixin, InvoicesMixin, CreditMixin):
    """Client for interacting with Lidl Connect Self-Care portal."""
    
    DASHBOARD_URL = "https://selfcare.lidl-connect.at/customer/dashboard/"
    
    def __init__(self, identifier: str, puk: str = None, password: str = None):
        """
        Initialize Lidl Connect client.
        
        Args:
            identifier: Your phone number or customer ID
            puk: Your PUK code (optional if password provided)
            password: Your password (optional if PUK provided)
        """
        # Base components
        self.identifier = identifier
        self.puk = puk
        self.password = password
        self.token = puk if puk else password
        
        # Session and tokens
        self.session = requests.Session()
        self.csrf_token = None
        self.endpoint_id = None
        self.logged_in = False
        
        # User data
        self.user_id = None
        
        atexit.register(self._cleanup)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _cleanup(self):
        """Clean up resources and log out when program exits."""
        if self.logged_in:
            try:
                self.logout()
            except Exception as e:
                print(f"Error during logout at program shutdown: {e}")
    
    def _signal_handler(self, signum, frame):
        """Handle termination signals to ensure clean logout."""
        print("\nCaught termination signal. Logging out...")
        self._cleanup()
        signal.signal(signum, signal.SIG_DFL)
        signal.raise_signal(signum)
    
    def initialize(self) -> bool:
        """
        Initialize the client: login, fetch dashboard, and extract necessary tokens and IDs.
        
        Returns:
            bool: True if initialization successful
        """
        if not self.login():
            return False
        
        try:
            soup = self._fetch_dashboard()
            self.csrf_token = self._extract_csrf(soup)
            self.user_id, self.endpoint_id = self._extract_user_and_endpoint(soup)
            return True
        except Exception as e:
            print(f"Error during initialization: {e}")
            return False
        
    def _fetch_dashboard(self):
        """Fetch dashboard HTML and parse it."""
        return self._get_soup(self.DASHBOARD_URL)