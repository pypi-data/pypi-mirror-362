"""
Unit tests for SAP BTP client.
"""
import pytest
from unittest.mock import patch
from open_logistics.infrastructure.external.sap_btp_client import SAPBTPClient

@pytest.mark.asyncio
async def test_authenticate_success():
    """Test successful authentication."""
    with patch('open_logistics.infrastructure.external.sap_btp_client.get_settings') as mock_get_settings:
        mock_get_settings.return_value.sap_btp.BTP_CLIENT_ID = "test_id"
        mock_get_settings.return_value.sap_btp.BTP_CLIENT_SECRET = "test_secret"
        mock_get_settings.return_value.sap_btp.BTP_AUTH_URL = "https://test.auth.url"
        
        client = SAPBTPClient()
        
        # Mock the HTTP client response
        with patch.object(client.client, 'post') as mock_post:
            mock_response = type('Response', (), {
                'json': lambda: {"access_token": "test_token", "expires_in": 3600},
                'raise_for_status': lambda: None
            })
            mock_post.return_value = mock_response
            
            token = await client.authenticate()
            assert token == "test_token"

@pytest.mark.asyncio
async def test_authenticate_failure():
    """Test failed authentication."""
    with patch('open_logistics.infrastructure.external.sap_btp_client.get_settings') as mock_get_settings:
        mock_get_settings.return_value.sap_btp.BTP_CLIENT_ID = ""
        client = SAPBTPClient()
        with pytest.raises(ValueError):
            await client.authenticate() 