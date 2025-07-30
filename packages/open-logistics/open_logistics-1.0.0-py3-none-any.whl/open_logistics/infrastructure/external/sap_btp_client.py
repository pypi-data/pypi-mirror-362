"""
Client for interacting with SAP Business Technology Platform (BTP).

This module provides comprehensive integration with SAP BTP services including
AI Core, HANA Cloud, Event Mesh, and other BTP services.
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

import httpx
from loguru import logger

from open_logistics.core.config import get_settings


class SAPBTPClient:
    """
    Handles communication with SAP BTP services, such as AI Core,
    HANA Cloud, and Event Mesh.
    
    Provides methods for:
    - OAuth 2.0 authentication
    - AI Core model deployment and inference
    - HANA Cloud database operations
    - Event Mesh business event publishing
    - Service management and monitoring
    """

    def __init__(self):
        self.settings = get_settings()
        self.client = httpx.AsyncClient(timeout=30.0)
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        
    async def authenticate(self) -> str:
        """
        Authenticates with SAP BTP using OAuth 2.0 flow.
        
        Returns:
            Access token for API calls
        """
        if not self.settings.sap_btp.BTP_CLIENT_ID:
            raise ValueError("SAP BTP client ID is not configured.")
            
        if not self.settings.sap_btp.BTP_CLIENT_SECRET:
            raise ValueError("SAP BTP client secret is not configured.")
            
        # Check if current token is still valid
        if self.access_token and self.token_expires_at and datetime.now() < self.token_expires_at:
            return self.access_token
            
        try:
            # OAuth 2.0 token endpoint
            token_url = f"{self.settings.sap_btp.BTP_AUTH_URL}/oauth/token"
            
            # Prepare authentication request
            auth_data = {
                "grant_type": "client_credentials",
                "client_id": self.settings.sap_btp.BTP_CLIENT_ID,
                "client_secret": self.settings.sap_btp.BTP_CLIENT_SECRET,
                "scope": "aicore:read aicore:write hana:read hana:write eventmesh:read eventmesh:write"
            }
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            
            # Make authentication request
            response = await self.client.post(token_url, data=auth_data, headers=headers)
            response.raise_for_status()
            
            # Parse response
            token_data = response.json()
            self.access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)  # 60s buffer
            
            logger.info("Successfully authenticated with SAP BTP")
            return self.access_token or ""
            
        except httpx.HTTPError as e:
            logger.error(f"SAP BTP authentication failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during SAP BTP authentication: {e}")
            raise
    
    async def deploy_ai_model(self, model_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deploy an AI model to SAP AI Core.
        
        Args:
            model_config: Model configuration including name, version, and parameters
            
        Returns:
            Deployment information
        """
        await self.authenticate()
        
        try:
            deployment_url = f"{self.settings.sap_btp.BTP_AI_CORE_URL}/v2/deployments"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            deployment_data = {
                "configurationId": model_config.get("configuration_id"),
                "resourceGroup": model_config.get("resource_group", "default"),
                "modelName": model_config.get("model_name"),
                "modelVersion": model_config.get("model_version", "1.0.0"),
                "parameters": model_config.get("parameters", {}),
                "metadata": {
                    "deployment_time": datetime.now().isoformat(),
                    "deployed_by": "open_logistics"
                }
            }
            
            response = await self.client.post(deployment_url, json=deployment_data, headers=headers)
            response.raise_for_status()
            
            deployment_result = response.json()
            logger.info(f"AI model deployed successfully: {deployment_result.get('id')}")
            
            return deployment_result
            
        except httpx.HTTPError as e:
            logger.error(f"AI model deployment failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during AI model deployment: {e}")
            raise
    
    async def run_inference(self, deployment_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run inference on a deployed AI model.
        
        Args:
            deployment_id: ID of the deployed model
            input_data: Input data for inference
            
        Returns:
            Inference results
        """
        await self.authenticate()
        
        try:
            inference_url = f"{self.settings.sap_btp.BTP_AI_CORE_URL}/v2/deployments/{deployment_id}/inference"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            inference_data = {
                "inputs": input_data,
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                "metadata": {
                    "inference_time": datetime.now().isoformat(),
                    "requested_by": "open_logistics"
                }
            }
            
            response = await self.client.post(inference_url, json=inference_data, headers=headers)
            response.raise_for_status()
            
            inference_result = response.json()
            logger.info(f"Inference completed successfully for deployment: {deployment_id}")
            
            return inference_result
            
        except httpx.HTTPError as e:
            logger.error(f"Inference failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during inference: {e}")
            raise
    
    async def publish_event(self, event_type: str, event_data: Dict[str, Any]) -> bool:
        """
        Publish a business event to SAP Event Mesh.
        
        Args:
            event_type: Type of the event
            event_data: Event payload
            
        Returns:
            True if event was published successfully
        """
        await self.authenticate()
        
        try:
            event_url = f"{self.settings.sap_btp.BTP_EVENT_MESH_URL}/events"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            event_payload = {
                "eventType": event_type,
                "eventVersion": "1.0",
                "eventTime": datetime.now().isoformat(),
                "source": "open_logistics",
                "data": event_data,
                "metadata": {
                    "correlation_id": f"ol_{int(datetime.now().timestamp())}",
                    "tenant": self.settings.sap_btp.BTP_TENANT_ID
                }
            }
            
            response = await self.client.post(event_url, json=event_payload, headers=headers)
            response.raise_for_status()
            
            logger.info(f"Event published successfully: {event_type}")
            return True
            
        except httpx.HTTPError as e:
            logger.error(f"Event publishing failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during event publishing: {e}")
            return False
    
    async def query_hana_cloud(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a query against SAP HANA Cloud.
        
        Args:
            query: SQL query to execute
            parameters: Query parameters
            
        Returns:
            Query results
        """
        await self.authenticate()
        
        try:
            hana_url = f"{self.settings.sap_btp.BTP_HANA_URL}/v1/query"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            query_data = {
                "query": query,
                "parameters": parameters or {},
                "metadata": {
                    "query_time": datetime.now().isoformat(),
                    "requested_by": "open_logistics"
                }
            }
            
            response = await self.client.post(hana_url, json=query_data, headers=headers)
            response.raise_for_status()
            
            query_result = response.json()
            logger.info(f"HANA Cloud query executed successfully")
            
            return query_result.get("results", [])
            
        except httpx.HTTPError as e:
            logger.error(f"HANA Cloud query failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during HANA Cloud query: {e}")
            raise
    
    async def get_service_status(self) -> Dict[str, Any]:
        """
        Get the status of various SAP BTP services.
        
        Returns:
            Service status information
        """
        await self.authenticate()
        
        service_status = {
            "authentication": "connected",
            "ai_core": "unknown",
            "hana_cloud": "unknown",
            "event_mesh": "unknown",
            "last_check": datetime.now().isoformat()
        }
        
        # Check AI Core status
        try:
            ai_core_url = f"{self.settings.sap_btp.BTP_AI_CORE_URL}/v2/health"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await self.client.get(ai_core_url, headers=headers)
            service_status["ai_core"] = "healthy" if response.status_code == 200 else "unhealthy"
        except Exception:
            service_status["ai_core"] = "unavailable"
        
        # Check HANA Cloud status
        try:
            hana_url = f"{self.settings.sap_btp.BTP_HANA_URL}/v1/health"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await self.client.get(hana_url, headers=headers)
            service_status["hana_cloud"] = "healthy" if response.status_code == 200 else "unhealthy"
        except Exception:
            service_status["hana_cloud"] = "unavailable"
        
        # Check Event Mesh status
        try:
            event_url = f"{self.settings.sap_btp.BTP_EVENT_MESH_URL}/health"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await self.client.get(event_url, headers=headers)
            service_status["event_mesh"] = "healthy" if response.status_code == 200 else "unhealthy"
        except Exception:
            service_status["event_mesh"] = "unavailable"
        
        return service_status
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
        
    async def __aenter__(self):
        """Async context manager entry."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close() 