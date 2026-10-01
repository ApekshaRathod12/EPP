"""Phone number utilities for normalizing and validating Indian phone numbers."""

import re
import logging

logger = logging.getLogger(__name__)

# India country code
COUNTRY_CODE = "91"
COUNTRY_PREFIX = f"+{COUNTRY_CODE}"


def normalize_phone(phone: str, country_code: str = COUNTRY_CODE) -> str:
    """
    Normalize a phone number to E.164 format (+91xxxxxxxxxx).

    Accepts:
    - +919876543210 (already normalized)
    - 919876543210 (without +)
    - 9876543210 (without country code)
    - 09876543210 (with leading 0)

    Args:
        phone: Phone number string
        country_code: Country code (default: 91 for India)

    Returns:
        Normalized phone number in E.164 format (+91xxxxxxxxxx)
        Returns None if invalid
    """

    if not phone:
        return None

    # Remove whitespace
    phone = str(phone).strip()

    # Remove any non-digit characters except +
    phone = re.sub(r'[^\d+]', '', phone)

    # Remove leading +
    if phone.startswith('+'):
        phone = phone[1:]

    # Handle different formats
    if phone.startswith('91'):
        # Already has country code
        phone = phone[2:]
    elif phone.startswith('0'):
        # Remove leading 0
        phone = phone[1:]

    # Validate: should be 10 digits for Indian numbers
    if not re.match(r'^\d{10}$', phone):
        logger.warning(f"Invalid phone number format: {phone}")
        return None

    # Return in E.164 format
    return f"+{country_code}{phone}"


def is_valid_phone(phone: str) -> bool:
    """Check if phone number is valid."""
    return normalize_phone(phone) is not None


def format_phone_display(phone: str) -> str:
    """Format phone for display (without + prefix)."""
    normalized = normalize_phone(phone)
    if normalized:
        return normalized.lstrip('+')
    return phone or "N/A"


def extract_phone_only(phone: str) -> str:
    """Extract just the 10-digit phone number (without country code)."""
    normalized = normalize_phone(phone)
    if normalized:
        return normalized.replace(f"+{COUNTRY_CODE}", "")
    return phone or ""


# Test cases
if __name__ == "__main__":
    test_numbers = [
        "+919876543210",
        "919876543210",
        "9876543210",
        "09876543210",
        "+91 98765 43210",
        "98-765-43210",
    ]

    for num in test_numbers:
        normalized = normalize_phone(num)
        print(f"{num:20} → {normalized}")
