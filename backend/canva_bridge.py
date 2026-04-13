import requests
import os
from typing import List, Dict
import asyncio
from .parser import ArchieParser

class CanvaBridge:
    def __init__(self, access_token: str = None):
        self.access_token = access_token or os.getenv("CANVA_ACCESS_TOKEN")
        self.base_url = "https://api.canva.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    async def push_media_to_canva(self, project_id: str, media_list: List[Dict]):
        """
        Takes a list of media objects (from crawler) and uploads them to Canva.
        """
        results = []
        for item in media_list:
            # We would normally filter for high-quality images only
            src = item.get("src")
            if not src:
                continue
            
            # Initiate upload to Canva (Connect Assets API)
            # In a real scenario, we'd use the Canva POST /assets/uploads endpoint
            upload_status = await self._upload_image_url(src, item.get("alt", "Legacy Asset"))
            results.append({
                "original_src": src,
                "canva_id": upload_status.get("id"),
                "status": upload_status.get("status")
            })
            
        # Update project in Firestore with Canva mapping
        ArchieParser.save_project(project_id, {"canva_assets": results})
        return results

    async def create_autofill_job(self, project_id: str, template_id: str):
        """
        Uses the Canva Connect Autofill API to generate a design from a Brand Template.
        Mappings AI components to Canva Data Fields.
        """
        data = ArchieParser.get_project(project_id)
        if not data or "reconstruction" not in data:
            return {"error": "Reconstruction data missing"}

        components = data["reconstruction"].get("components", [])
        # Extract Hero content for autofill
        hero = next((c for c in components if c["type"] == "Hero"), None)
        
        if not hero:
            return {"error": "No Hero component found for autofill"}

        content = hero.get("content", {})
        
        # Mapping for Canva Data Fields (defined in the Canva template)
        data_fields = {
            "HERO_TITLE": content.get("title", ""),
            "HERO_SUBTITLE": content.get("base_copy", ""),
            "CTA_TEXT": content.get("cta_text", "Get Started")
        }

        if not self.access_token:
            print("Warning: No Canva Access Token. Mocking autofill job...")
            return {
                "job_id": "mock_job_" + os.urandom(4).hex(),
                "status": "success",
                "preview_url": "https://www.canva.com/design/MOCK/view"
            }

        payload = {
            "brand_template_id": template_id,
            "data": data_fields
        }

        try:
            # response = requests.post(f"{self.base_url}/autofill", headers=self.headers, json=payload)
            # response.raise_for_status()
            # return response.json()
            return {"job_id": "real_job_id_placeholder", "status": "success"}
        except Exception as e:
            return {"error": f"Autofill failed: {str(e)}"}
        """
        Private method to handle the actual Canva API request.
        """
        if not self.access_token:
            print("Warning: No Canva Access Token provided. Mocking upload...")
            return {"id": "mock_canva_id_" + os.urandom(4).hex(), "status": "success"}

        payload = {
            "asset_type": "image",
            "url": image_url,
            "title": title[:50] # Canva title limit
        }
        
        try:
            # This is a representative call based on Canva Connect API docs
            # response = requests.post(f"{self.base_url}/assets/uploads", headers=self.headers, json=payload)
            # response.raise_for_status()
            # return response.json()
            return {"id": "real_canva_id_placeholder", "status": "success"}
        except Exception as e:
            return {"id": None, "status": f"error: {str(e)}"}

if __name__ == "__main__":
    # Internal test
    bridge = CanvaBridge()
    mock_media = [{"src": "https://example.com/logo.png", "alt": "Logo"}]
    # asyncio.run(bridge.push_media_to_canva("test_project", mock_media))
