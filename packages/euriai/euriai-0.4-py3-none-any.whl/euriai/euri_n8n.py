import requests
from typing import Any, Dict, Optional

class EuriaiN8N:
    """
    Wrapper for n8n workflow automation integration in the EURI SDK.
    Allows triggering n8n workflows and exchanging data via REST API.
    """
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the n8n wrapper.
        Args:
            base_url: Base URL of the n8n instance (e.g., http://localhost:5678 or cloud URL)
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key

    def trigger_workflow(self, workflow_id: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Trigger an n8n workflow by ID, optionally passing data.
        Returns the workflow execution response.
        """
        url = f"{self.base_url}/webhook/{workflow_id}"
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        response = requests.post(url, json=data or {}, headers=headers)
        response.raise_for_status()
        return response.json() 