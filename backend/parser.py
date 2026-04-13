import os
import json
import logging
import firebase_admin
from firebase_admin import firestore
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Initialize Firebase using Application Default Credentials (ADC) or
# a service account key file pointed to by GOOGLE_APPLICATION_CREDENTIALS.
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()

try:
    db = firestore.client()
except Exception as e:
    logger.warning("Firestore client could not be initialized: %s", e)
    db = None

# Configure LLM (Gemini)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')

class ArchieParser:
    @staticmethod
    async def reconstruct_page(html_content: str):
        prompt = f"""
        You are 'Archie - The Web Butler', the world's most advanced AI Content Reconstruction System.
        Goal: Analyze legacy HTML and extract 'Clean Component Skeletons' for a modern CMS migration.

        RULES:
        1. Ignore legacy styling (inline CSS, fonts, background-colors).
        2. Identify the 'Core Intent' of each section.
        3. Map content to these Component Types: Hero, FeatureList, TestimonialTable, ContactCard, NarrativeBlock.
        4. Fix casing and typos in the extracted text.
        5. Group media assets with their respective components.

        OUTPUT SCHEMA:
        {{
          "sitemap_proposal": "string (slug)",
          "components": [
            {{
              "type": "Hero",
              "content": {{ "title": "...", "base_copy": "...", "cta_text": "..." }},
              "assets": ["img_url_1"]
            }}
          ],
          "metadata": {{ "last_modernized": "iso-date", "original_url": "..." }}
        }}

        Legacy HTML:
        {html_content[:7000]} 

        Output EXACT JSON only.
        """
        
        response = await model.generate_content_async(prompt)
        try:
            json_str = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(json_str)
        except Exception as e:
            return {"error": "Failed to parse AI response", "raw": response.text}

    @staticmethod
    def save_project(project_id: str, data: dict):
        if db is None:
            raise RuntimeError("Firestore is not initialized. Check GOOGLE_APPLICATION_CREDENTIALS.")
        doc_ref = db.collection("projects").document(project_id)
        doc_ref.set(data, merge=True)
        return project_id

    @staticmethod
    def get_project(project_id: str):
        if db is None:
            raise RuntimeError("Firestore is not initialized. Check GOOGLE_APPLICATION_CREDENTIALS.")
        doc_ref = db.collection("projects").document(project_id)
        return doc_ref.get().to_dict()
