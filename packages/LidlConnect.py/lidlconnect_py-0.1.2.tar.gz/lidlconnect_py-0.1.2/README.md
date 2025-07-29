# LidlConnect.py

[![PyPI version](https://badge.fury.io/py/LidlConnect.py.svg)](https://badge.fury.io/py/LidlConnect.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library for accessing your Lidl Connect account through the Self-Care API.

## Features

- 📱 View your current data, minutes, and SMS usage
- 💰 Check your account balance and payment history
- 📅 View tariff details and package validity dates
- 🧾 Access invoice and voucher history
- 🔄 Automatic session management with proper login/logout

## Installation

Install directly from PyPI:

```bash
pip install LidlConnect.py
```

## Quick Start

```python
from LidlConnect import LidlConnect

# Initialize with PUK (preferred method)
client = LidlConnect(identifier="069012345678", puk="12345678")

# Or initialize with password
# client = LidlConnect(identifier="069012345678", password="yourPassword")

# Login and initialize connection
if not client.initialize():
    print("Failed to initialize client")
    exit(1)

# Get remaining data
data_info = client.get_remaining_data()
print(f"Data: {data_info['remaining']}/{data_info['total']} GiB")

# Check minutes
minutes_info = client.get_remaining_minutes()
print(f"Minutes: {minutes_info['remaining']}/{minutes_info['total']} minutes")

# Get EU roaming data
eu_data_info = client.get_remaining_eu_data()
print(f"EU Data: {eu_data_info['remaining']}/{eu_data_info['total']} GiB")

# Access account information
print(f"User: {client.user_name}")
print(f"Phone Number: {client.phone_number}")
print(f"Balance: €{client.balance if client.balance is not None else 'N/A'}")
print(f"Package valid until: {client.tariff_package_valid_to}")

# View payment history
client.print_invoices()

# Logout when done (automatic on program exit, but explicit is better)
client.logout()
```

## Documentation

For complete documentation of all features and methods, please refer to the [API documentation](apiDoc.md).

## Requirements

- Python 3.6+
- `requests` library
- `beautifulsoup4` library

## Supported Services

This library currently supports the Austrian Lidl Connect service (https://selfcare.lidl-connect.at). It's designed to work with accounts that have at least one active tariff package.

## License

MIT License

## Disclaimer

This is an unofficial library and is not affiliated with, maintained, authorized, endorsed, or sponsored by Lidl or any of its affiliates (like Drei).
