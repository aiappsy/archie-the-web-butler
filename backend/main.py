from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from .crawler import ArchieCrawler
from .parser import ArchieParser
from .canva_bridge import CanvaBridge
from .webflow_connector import WebflowConnector
from .report_generator import ReportGenerator
from typing import Literal
from urllib.parse import urlparse
import ipaddress
import uuid
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Archie - The Web Butler Backend")

# ---------------------------------------------------------------------------
# CORS – allow only the origins listed in ALLOWED_ORIGINS (comma-separated).
# Wildcard ("*") must never be combined with allow_credentials=True.
# ---------------------------------------------------------------------------
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated PDF reports as static files
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)
app.mount("/reports", StaticFiles(directory=REPORTS_DIR), name="reports")

# ---------------------------------------------------------------------------
# SSRF guard helpers
# ---------------------------------------------------------------------------
_PRIVATE_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # link-local / AWS metadata
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
]

def _is_safe_url(url: str) -> bool:
    """Return True only for public HTTP/HTTPS URLs."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        host = parsed.hostname
        if not host:
            return False
        try:
            addr = ipaddress.ip_address(host)
            return not any(addr in net for net in _PRIVATE_RANGES)
        except ValueError:
            # hostname – basic checks for localhost variants
            if host.lower() in ("localhost", "metadata.google.internal"):
                return False
        return True
    except Exception:
        return False


@app.get("/")
async def root():
    return {"message": "Archie Backend is active"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# Ingestion API
@app.post("/ingest")
async def ingest_url(url: str, background_tasks: BackgroundTasks):
    if not _is_safe_url(url):
        raise HTTPException(status_code=400, detail="Invalid or disallowed URL.")

    project_id = str(uuid.uuid4())
    background_tasks.add_task(run_crawl_audit, project_id, url)
    
    return {
        "project_id": project_id,
        "message": "Crawling and Audit initiated",
        "monitor_url": f"/audit/{project_id}"
    }

async def run_crawl_audit(project_id: str, url: str):
    try:
        crawler = ArchieCrawler(url)
        results = await crawler.crawl(max_pages=20)
        ArchieParser.save_project(project_id, {
            "url": url,
            "status": "audited",
            "results": results
        })
    except Exception as e:
        logger.error("Background crawl failed for project %s: %s", project_id, e)

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
_ALLOWED_STATUSES = {"pending", "accepted", "rejected", "flagged"}

@app.patch("/projects/{project_id}/components/{index}")
async def update_component_status(
    project_id: str, index: int, status: Literal["pending", "accepted", "rejected", "flagged"]
):
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
    os.makedirs(REPORTS_DIR, exist_ok=True)
    file_name = f"audit_{project_id[:8]}.pdf"
    file_path = os.path.join(REPORTS_DIR, file_name)
    
    result = ReportGenerator.generate_audit_report(project_id, file_path)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return {"message": "Report generated successfully", "download_url": f"/reports/{file_name}"}

