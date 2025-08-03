import os
import uuid
import tempfile
import json
from typing import Dict, Any, Optional
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
rule_engine = None
print("Starting CloseGuard API...")

def init_rule_engine():
    global rule_engine
    try:
        import os
        print(f"Current working directory: {os.getcwd()}")
        print(f"Files in directory: {os.listdir('.')}")
        
        config_path = os.path.join(os.path.dirname(__file__), "rules-config.yaml")
        print(f"Looking for rules config at: {config_path}")
        
        if os.path.exists(config_path):
            rule_engine = RuleEngine(config_path)
            print(f"Rule engine initialized successfully with {len(rule_engine.rules)} rules")
        else:
            print(f"Rules config file not found at {config_path}")
            # Try current directory as fallback
            if os.path.exists("rules-config.yaml"):
                rule_engine = RuleEngine("rules-config.yaml")
                print(f"Rule engine initialized from current directory with {len(rule_engine.rules)} rules")
            else:
                print("No rules config found - continuing without rules")
    except Exception as e:
        print(f"Warning: Failed to initialize rule engine: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()

# Initialize at startup
init_rule_engine()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "CloseGuard API is running"}


class UserContext(BaseModel):
    expectedLoanType: str = 'Not sure'
    expectedInterestRate: Optional[float] = None
    expectedClosingCosts: Optional[float] = None
    promisedZeroClosingCosts: bool = False
    promisedLenderCredit: Optional[float] = None
    promisedSellerCredit: Optional[float] = None
    promisedRebate: Optional[float] = None
    usedBuildersPreferredLender: bool = False
    builderName: Optional[str] = None
    builderPromisedToCoverTitleFees: bool = False
    builderPromisedToCoverEscrowFees: bool = False
    builderPromisedToCoverInspection: bool = False
    hadBuyerAgent: bool = False
    buyerAgentName: Optional[str] = None
    expectedMortgageInsurance: bool = False
    expectedMortgageInsuranceAmount: Optional[float] = None
    expectedPurchasePrice: Optional[float] = None
    expectedLoanAmount: Optional[float] = None

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    context: str = Form(None)
):
    """
    Upload a PDF file for analysis with optional user context.
    
    Args:
        file: PDF file to analyze
        context: JSON string of user expectations and promises
    
    Returns:
        JSON response with report_id
    """
    print(f"=== UPLOAD DEBUG ===")
    print(f"File: {file.filename}")
    print(f"Content-Type: {file.content_type}")
    print(f"Size: {file.size if hasattr(file, 'size') else 'unknown'}")
    print(f"Context: {context}")
    
    # Validate file type
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        print(f"ERROR: Invalid filename: {file.filename}")
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    if not file.content_type or file.content_type != 'application/pdf':
        print(f"ERROR: Invalid content type: {file.content_type}")
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
            print(f"Extracting text from: {temp_file_path}")
            extracted_text = extract_text(temp_file_path)
            print(f"Extracted {len(extracted_text)} characters")
            
            if not extracted_text.strip():
                print("ERROR: No text extracted from PDF")
                raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")
            
            # Parse user context if provided
            user_context = None
            if context:
                try:
                    context_data = json.loads(context)
                    user_context = UserContext(**context_data)
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"Warning: Failed to parse user context: {e}")
            
            # Run rule engine analysis
            flags = []
            if rule_engine:
                if user_context:
                    flags = rule_engine.check_text_with_context(extracted_text, user_context.dict())
                else:
                    flags = rule_engine.check_text(extracted_text)
            
            # Calculate forensic analytics
            forensic_score = rule_engine.calculate_forensic_score(flags) if rule_engine else 100
            severity_counts = rule_engine.categorize_flags_by_severity(flags) if rule_engine else {'high': 0, 'medium': 0, 'low': 0}
            
            # Store report in memory
            reports_store[report_id] = {
                "status": "done",
                "flags": flags,
                "filename": file.filename,
                "text_length": len(extracted_text),
                "user_context": user_context.dict() if user_context else None,
                "forensic_score": forensic_score,
                "total_flags": len(flags),
                "high_severity": severity_counts['high'],
                "medium_severity": severity_counts['medium'],
                "low_severity": severity_counts['low']
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
            "analytics": {
                "forensic_score": report.get("forensic_score", 100),
                "total_flags": report.get("total_flags", 0),
                "high_severity": report.get("high_severity", 0),
                "medium_severity": report.get("medium_severity", 0),
                "low_severity": report.get("low_severity", 0)
            },
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
    uvicorn.run("main:app", host="0.0.0.0", port=port)