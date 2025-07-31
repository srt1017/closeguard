import os
import uuid
import tempfile
from typing import Dict, Any
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from parser import extract_text
from engine import RuleEngine


# Initialize FastAPI app
app = FastAPI(
    title="CloseGuard API",
    description="MVP backend for analyzing home-closing PDFs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporarily allow all for debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for reports
reports_store: Dict[str, Dict[str, Any]] = {}

# Initialize rule engine
try:
    import os
    config_path = os.path.join(os.path.dirname(__file__), "rules-config.yaml")
    rule_engine = RuleEngine(config_path)
    print(f"Rule engine initialized successfully with {len(rule_engine.rules)} rules")
except Exception as e:
    print(f"Warning: Failed to initialize rule engine: {e}")
    rule_engine = None


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "CloseGuard API is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file for analysis.
    
    Returns:
        JSON response with report_id
    """
    # Validate file type
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    if not file.content_type or file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Invalid content type. Expected application/pdf")
    
    # Generate unique report ID
    report_id = str(uuid.uuid4())
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            # Read and save uploaded file
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Extract text from PDF
            extracted_text = extract_text(temp_file_path)
            
            if not extracted_text.strip():
                raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")
            
            # Run rule engine analysis
            flags = []
            if rule_engine:
                flags = rule_engine.check_text(extracted_text)
            
            # Store report in memory
            reports_store[report_id] = {
                "status": "done",
                "flags": flags,
                "filename": file.filename,
                "text_length": len(extracted_text)
            }
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass
        
        return JSONResponse(
            status_code=200,
            content={"report_id": report_id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")


@app.get("/report/{report_id}")
async def get_report(report_id: str):
    """
    Get analysis report by report ID.
    
    Args:
        report_id: UUID of the report
        
    Returns:
        JSON response with status and flags
    """
    if report_id not in reports_store:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report = reports_store[report_id]
    
    return JSONResponse(
        status_code=200,
        content={
            "status": report["status"],
            "flags": report["flags"],
            "metadata": {
                "filename": report.get("filename"),
                "text_length": report.get("text_length")
            }
        }
    )


@app.get("/reports")
async def list_reports():
    """
    List all available reports (for debugging/admin purposes).
    
    Returns:
        JSON response with all report IDs and their status
    """
    report_summary = {}
    for report_id, report in reports_store.items():
        report_summary[report_id] = {
            "status": report["status"],
            "flags_count": len(report["flags"]),
            "filename": report.get("filename")
        }
    
    return JSONResponse(
        status_code=200,
        content={"reports": report_summary}
    )


@app.delete("/report/{report_id}")
async def delete_report(report_id: str):
    """
    Delete a report from memory.
    
    Args:
        report_id: UUID of the report to delete
        
    Returns:
        JSON response confirming deletion
    """
    if report_id not in reports_store:
        raise HTTPException(status_code=404, detail="Report not found")
    
    del reports_store[report_id]
    
    return JSONResponse(
        status_code=200,
        content={"message": f"Report {report_id} deleted successfully"}
    )


# Exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)