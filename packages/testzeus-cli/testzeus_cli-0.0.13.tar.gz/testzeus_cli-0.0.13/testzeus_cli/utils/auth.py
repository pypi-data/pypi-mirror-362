"""
Authentication utility functions for the TestZeus CLI.
"""

import base64
import json
from testzeus_sdk import TestZeusClient
from typing import Dict, Any, Optional, cast


def decode_jwt_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode a JWT token payload.

    Args:
        token: The JWT token

    Returns:
        Decoded payload as a dictionary, or None if decoding fails
    """
    try:
        # For JWT tokens
        token_parts = token.split(".")
        if len(token_parts) == 3:  # Standard JWT format
            # Decode the payload (middle part)
            payload = token_parts[1]
            # Add padding if needed
            padding = "=" * (4 - len(payload) % 4)
            payload += padding
            # Decode from base64
            decoded = base64.b64decode(payload.replace("-", "+").replace("_", "/"))
            return cast(Dict[str, Any], json.loads(decoded))
    except Exception:
        pass

    return None


def initialize_client_with_token(client: TestZeusClient, token: str) -> None:
    """
    Initialize a TestZeusClient with a token, properly setting up the auth store model.

    Args:
        client: The TestZeusClient instance
        token: JWT token
    """
    # Set the token
    client.token = token
    client._authenticated = True

    # Extract token data
    claims = decode_jwt_payload(token)
    tenant_id = None
    user_id = None

    if claims:
        # Check for tenant ID in various possible locations within the token
        if "tenant" in claims:
            tenant_id = claims["tenant"]
        elif "record" in claims and "tenant" in claims["record"]:
            tenant_id = claims["record"]["tenant"]
        elif "collectionId" in claims and claims["collectionId"] != "_pb_users_auth_":
            # Use collection ID as a fallback if it's not the default auth collection
            tenant_id = claims["collectionId"]

        # Extract user ID from the token
        if "id" in claims:
            user_id = claims["id"]
        elif "sub" in claims:
            user_id = claims["sub"]
        elif "record" in claims and "id" in claims["record"]:
            user_id = claims["record"]["id"]

    # Save the token to the auth store - this should properly populate auth_store.model
    client.pb.auth_store.save(token, None)

    # Try to set user_id on the auth model if it exists and we have a user_id
    if user_id and client.pb.auth_store.model:
        try:
            # Try to set the ID on the existing model
            if hasattr(client.pb.auth_store.model, "id"):
                client.pb.auth_store.model.id = user_id
            else:
                # Add ID attribute to existing model
                setattr(client.pb.auth_store.model, "id", user_id)
        except Exception:
            # If we can't set the model, that's okay - the SDK might handle it differently
            pass

    # Only set a tenant ID if we found a valid one (not the default PocketBase authentication one)
    if tenant_id and tenant_id != "_pb_users_auth_" and tenant_id != "pbc_138639755":
        # Add tenant ID directly to the client for easy access
        setattr(client, "_tenant_id", tenant_id)
    else:
        # Try to get tenant from test if this is a test-related token
        if claims and "test" in claims:
            # We'll try to resolve the tenant from the test itself
            # This would require additional API calls, handled in the command functions
            setattr(client, "_tenant_id", "")
        else:
            # Set empty tenant ID to indicate we need to resolve it from context
            setattr(client, "_tenant_id", "")


def extract_tenant_from_token(token: str) -> str:
    """
    Extract tenant ID from a JWT token.

    Args:
        token: The JWT token

    Returns:
        Tenant ID or empty string if not found
    """
    claims = decode_jwt_payload(token)

    if claims:
        # Check for tenant ID in various possible locations
        if "tenant" in claims:
            return str(claims["tenant"])
        elif "record" in claims and "tenant" in claims["record"]:
            return str(claims["record"]["tenant"])
        elif "collectionId" in claims:
            return str(claims["collectionId"])
        # Look for tenant in other possible locations
        elif (
            "record" in claims
            and claims["record"].get("collectionId")
            and claims["record"]["collectionId"] != "_pb_users_auth_"
        ):
            return str(claims["record"]["collectionId"])

    # No default value - let the API determine the appropriate tenant
    return ""
