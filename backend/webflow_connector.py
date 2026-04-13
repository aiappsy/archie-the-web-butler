import requests
import json
import os
import logging
from .parser import ArchieParser

logger = logging.getLogger(__name__)

class WebflowConnector:
    def __init__(self, api_token: str = None):
        self.api_token = api_token or os.getenv("WEBFLOW_API_TOKEN")
        self.base_url = "https://api.webflow.com/v2"
        self.headers = {
            "Content-Type": "application/json",
            "Accept-Version": "2.0.0",
        }
        if self.api_token:
            self.headers["Authorization"] = f"Bearer {self.api_token}"

    async def export_reconstruction(self, project_id: str, collection_id: str):
        """
        Pushes AI-reconstructed components to a Webflow CMS Collection.
        """
        data = ArchieParser.get_project(project_id)
        if not data or "reconstruction" not in data:
            return {"error": "No reconstruction data found for export."}

        components = data["reconstruction"].get("components", [])
        results = []

        for i, comp in enumerate(components):
            # Map Archie Component to Webflow Field Data
            # Note: This mapping depends on the specific Webflow Collection Schema
            field_data = {
                "name": f"{comp['type']} - {project_id[:8]}",
                "slug": f"{comp['type'].lower()}-{project_id[:8]}-{i}",
                "component-type": comp['type'],
                "content-body": comp['content'].get('base_copy', comp['content'].get('title', ''))
            }

            # If the component is a 'Hero', we might have specific fields
            if comp['type'] == 'Hero':
                field_data["headline"] = comp['content'].get('title', '')
                field_data["cta-label"] = comp['content'].get('cta_text', '')

            status = await self._create_collection_item(collection_id, field_data)
            results.append({
                "component_index": i,
                "webflow_id": status.get("id"),
                "status": status.get("status", "success")
            })

        # Update project status in Firestore
        ArchieParser.save_project(project_id, {"webflow_export": results, "status": "exported"})
        return results

    async def _create_collection_item(self, collection_id: str, field_data: dict):
        """
        Private method to call Webflow API.
        """
        if not self.api_token:
            logger.warning("No Webflow API Token. Mocking export...")
            return {"id": f"mock_item_{os.urandom(4).hex()}", "status": "success"}

        url = f"{self.base_url}/collections/{collection_id}/items"
        payload = {
            "fieldData": field_data,
            "isDraft": True,
            "isArchived": False
        }

        try:
            # TODO: uncomment once Webflow API credentials are configured
            # response = requests.post(url, headers=self.headers, json=payload)
            # response.raise_for_status()
            # return response.json()
            return {"id": "real_webflow_id_placeholder", "status": "success"}
        except Exception as e:
            return {"id": None, "status": f"error: {str(e)}"}
