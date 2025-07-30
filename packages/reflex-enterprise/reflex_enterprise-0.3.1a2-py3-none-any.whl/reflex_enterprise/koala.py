"""Koala Analytics integration for user identification."""

from datetime import datetime, timezone
from typing import Any

import httpx
from reflex.config import get_config
from reflex.utils.prerequisites import ensure_reflex_installation_id

from . import constants


def identify_koala_user(email: str, extra_data: dict[str, Any] | None = None) -> bool:
    """Identify a user to Koala Analytics.

    Args:
        email: User's email address
        extra_data: Additional user properties to send

    Returns:
        True if the identification was successful, False otherwise
    """
    # Check if telemetry is enabled
    if not get_config().telemetry_enabled:
        return False

    # Get persistent user ID from Reflex installation
    if not (ko_id := str(ensure_reflex_installation_id() or "")):
        return False
    timestamp = datetime.now(timezone.utc).isoformat()

    payload = {
        "ko_id": ko_id,
        "email": email,
        "timestamp": timestamp,
        "traits": {
            "reflex_enterprise": True,
            **(extra_data or {}),
        },
    }

    # Send to Koala API
    api_url = constants.KOALA_API_ENDPOINT.format(constants.KOALA_PUBLIC_API_KEY)

    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.post(
                api_url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            return True
    except Exception:
        return False
