from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from .crawler import ArchieCrawler
from .parser import ArchieParser
from .canva_bridge import CanvaBridge
from .webflow_connector import WebflowConnector
from .report_generator import ReportGenerator
import uuid
import asyncio
import os

app = FastAPI(title="Archie - The Web Butler Backend")

# Configure CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Archie Backend is active"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# Ingestion API
@app.post("/ingest")
async def ingest_url(url: str, background_tasks: BackgroundTasks):
    project_id = str(uuid.uuid4())
    
    # Run crawl in background
    background_tasks.add_task(run_crawl_audit, project_id, url)
    
    return {
        "project_id": project_id,
        "message": "Crawling and Audit initiated",
        "monitor_url": f"/audit/{project_id}"
    }

async def run_crawl_audit(project_id: str, url: str):
    crawler = ArchieCrawler(url)
    results = await crawler.crawl(max_pages=20)
    
    # Save to Firestore
    ArchieParser.save_project(project_id, {
        "url": url,
        "status": "audited",
        "results": results
    })

# Canva Integration API
@app.post("/projects/{project_id}/push-to-canva")
async def push_to_canva(project_id: str):
    data = ArchieParser.get_project(project_id)
    if not data or "results" not in data:
        raise HTTPException(status_code=404, detail="Project or Media not found")
    
    media_list = data["results"].get("media", [])
    if not media_list:
        return {"message": "No media found in this project to push."}
    
    bridge = CanvaBridge()
    results = await bridge.push_media_to_canva(project_id, media_list)
    
    return {
        "message": f"Successfully processed {len(results)} assets for Canva.",
        "results": results
    }

# Human-in-the-Loop Component Review API
@app.patch("/projects/{project_id}/components/{index}")
async def update_component_status(project_id: str, index: int, status: str):
    data = ArchieParser.get_project(project_id)
    if not data or "reconstruction" not in data:
        raise HTTPException(status_code=404, detail="Project or Reconstruction not found")
    
    components = data["reconstruction"].get("components", [])
    if index >= len(components):
        raise HTTPException(status_code=400, detail="Component index out of range")
    
    components[index]["status"] = status
    ArchieParser.save_project(project_id, {"reconstruction": {"components": components}})
    
    return {"message": f"Component {index} marked as {status}", "status": status}

# Canva Marketing Autofill API
@app.post("/projects/{project_id}/generate-marketing-assets")
async def generate_marketing_assets(project_id: str, template_id: str):
    bridge = CanvaBridge()
    result = await bridge.create_autofill_job(project_id, template_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

# Webflow Export API
@app.post("/projects/{project_id}/export-webflow")
async def export_to_webflow(project_id: str, collection_id: str):
    connector = WebflowConnector()
    results = await connector.export_reconstruction(project_id, collection_id)
    
    if "error" in results:
        raise HTTPException(status_code=400, detail=results["error"])
        
    return results

# PDF Reporting API
@app.get("/projects/{project_id}/report")
async def get_project_report(project_id: str):
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    file_path = f"{output_dir}/audit_{project_id[:8]}.pdf"
    
    result = ReportGenerator.generate_audit_report(project_id, file_path)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return {"message": "Report generated successfully", "download_url": f"/{file_path}"}
