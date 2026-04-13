import os
import json
from firebase_admin import credentials, firestore, initialize_app
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase
# Note: User needs to provide serviceAccountKey.json or use ADC
try:
    if not len(initialize_app()):
        initialize_app()
except:
    pass

db = firestore.client()

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
        
        response = model.generate_content(prompt)
        try:
            json_str = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(json_str)
        except Exception as e:
            return {"error": "Failed to parse AI response", "raw": response.text}

    @staticmethod
    def save_project(project_id: str, data: dict):
        doc_ref = db.collection("projects").document(project_id)
        doc_ref.set(data, merge=True)
        return project_id

    @staticmethod
    def get_project(project_id: str):
        doc_ref = db.collection("projects").document(project_id)
        return doc_ref.get().to_dict()
