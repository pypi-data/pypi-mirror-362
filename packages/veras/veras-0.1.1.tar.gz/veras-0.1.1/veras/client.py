"""
Veras AI Compliance Platform Python SDK Client

This module provides the main client interface for interacting with the Veras API.
"""

import requests
from typing import Dict, Any, Optional
from .exceptions import VerasError


class VerasClient:
    """
    Main client for interacting with the Veras AI Compliance Platform.
    
    This client provides methods for creating traces, verifying them on the blockchain,
    and managing audit trails.
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.veras.com"):
        """
        Initialize the Veras client.
        
        Args:
            api_key: Your Veras API key
            base_url: Base URL for the Veras API (defaults to production)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'Veras-Python-SDK/0.1.0'
        })
    
    def create_trace(self, data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new audit trace.
        
        Args:
            data: The data to be traced (will be redacted according to rules)
            metadata: Optional metadata about the trace
            
        Returns:
            Dictionary containing trace information including ID
            
        Raises:
            VerasError: If the API request fails
        """
        payload = {
            'data': data,
            'metadata': metadata or {}
        }
        
        try:
            response = self.session.post(f"{self.base_url}/traces", json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise VerasError(f"Failed to create trace: {str(e)}")
    
    def verify_trace(self, trace_id: str) -> Dict[str, Any]:
        """
        Verify a trace on the blockchain.
        
        Args:
            trace_id: The ID of the trace to verify
            
        Returns:
            Dictionary containing verification status and blockchain info
            
        Raises:
            VerasError: If the API request fails
        """
        try:
            response = self.session.get(f"{self.base_url}/traces/{trace_id}/verify")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise VerasError(f"Failed to verify trace: {str(e)}")
    
    def get_trace(self, trace_id: str) -> Dict[str, Any]:
        """
        Retrieve a trace by ID.
        
        Args:
            trace_id: The ID of the trace to retrieve
            
        Returns:
            Dictionary containing trace information
            
        Raises:
            VerasError: If the API request fails
        """
        try:
            response = self.session.get(f"{self.base_url}/traces/{trace_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise VerasError(f"Failed to get trace: {str(e)}")
