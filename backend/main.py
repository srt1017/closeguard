"""
Updated CloseGuard API using the new modular architecture.
This maintains full API compatibility while using the new services.
"""

import os
import uuid
import json
import time
from typing import Dict, Any, Optional
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import new services
from services.analysis import RuleEngineService, ScoringService, ValidationService
from services.parsing import DocumentParserService
from models.core import UserContext as UserContextModel, Report, ReportMetadata
from config.settings import Settings


# Initialize settings
settings = Settings.from_env()

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)

# In-memory store for reports (same as before for compatibility)
reports_store: Dict[str, Dict[str, Any]] = {}

# Initialize services
rule_engine_service = None
scoring_service = None
document_parser_service = None
validation_service = None

print("Starting CloseGuard API v2 with modular architecture...")


def init_services():
    """Initialize all services."""
    global rule_engine_service, scoring_service, document_parser_service, validation_service
    
    try:
        # Find rules config file
        config_path = os.path.join(os.path.dirname(__file__), "rules-config.yaml")
        if not os.path.exists(config_path):
            config_path = "rules-config.yaml"
        
        print(f"Looking for rules config at: {config_path}")
        
        # Initialize services
        rule_engine_service = RuleEngineService(config_path)
        scoring_service = ScoringService(
            max_score=settings.max_forensic_score,
            severity_weights=settings.severity_weights
        )
        document_parser_service = DocumentParserService(settings.temp_dir)
        validation_service = ValidationService()
        
        # Validate rules configuration
        validation_result = rule_engine_service.validate_rules_config()
        if validation_result['valid']:
            print(f"Services initialized successfully with {validation_result['rules_count']} rules")
            if validation_result['warnings']:
                print(f"Warnings: {validation_result['warnings']}")
        else:
            print(f"WARNING: Rules validation failed: {validation_result['errors']}")
            
    except Exception as e:
        print(f"ERROR: Failed to initialize services: {e}")
        import traceback
        traceback.print_exc()


# Initialize services at startup
init_services()


# Pydantic model for API compatibility (matches original)
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


def convert_api_context_to_model(api_context: UserContext) -> UserContextModel:
    """Convert API UserContext to internal model."""
    return UserContextModel(
        expected_loan_type=api_context.expectedLoanType,
        expected_interest_rate=api_context.expectedInterestRate,
        expected_closing_costs=api_context.expectedClosingCosts,
        promised_zero_closing_costs=api_context.promisedZeroClosingCosts,
        promised_lender_credit=api_context.promisedLenderCredit,
        promised_seller_credit=api_context.promisedSellerCredit,
        promised_rebate=api_context.promisedRebate,
        used_builders_preferred_lender=api_context.usedBuildersPreferredLender,
        builder_name=api_context.builderName,
        builder_promised_to_cover_title_fees=api_context.builderPromisedToCoverTitleFees,
        builder_promised_to_cover_escrow_fees=api_context.builderPromisedToCoverEscrowFees,
        builder_promised_to_cover_inspection=api_context.builderPromisedToCoverInspection,
        has_buyer_agent_representation=api_context.hadBuyerAgent,
        buyer_agent_name=api_context.buyerAgentName,
        expected_purchase_price=api_context.expectedPurchasePrice,
        expected_loan_amount=api_context.expectedLoanAmount
    )


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "CloseGuard API v2 is running"}


@app.get("/health")
async def health_check():
    """Detailed health check with service status."""
    return {
        "status": "healthy",
        "services": {
            "rule_engine": rule_engine_service is not None,
            "scoring_service": scoring_service is not None,
            "document_parser": document_parser_service is not None,
            "validation_service": validation_service is not None
        },
        "rules_summary": rule_engine_service.get_rules_summary() if rule_engine_service else None
    }


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
    start_time = time.time()
    
    print(f"=== UPLOAD DEBUG ===")
    print(f"File: {file.filename}")
    print(f"Content-Type: {file.content_type}")
    print(f"Context: {context}")
    
    # Validate file using validation service
    file_size = 0
    if hasattr(file, 'size'):
        file_size = file.size
    
    validation_result = validation_service.validate_file_upload(
        file.filename, 
        file_size, 
        settings.max_file_size
    )
    
    if not validation_result['valid']:
        raise HTTPException(status_code=400, detail=validation_result['errors'][0])
    
    # Generate unique report ID
    report_id = str(uuid.uuid4())
    
    try:
        # Read file content
        content = await file.read()
        
        # Extract text using document parser service
        print(f"Extracting text from uploaded file...")
        extracted_text = document_parser_service.extract_text_from_upload(content, file.filename)
        print(f"Extracted {len(extracted_text)} characters")
        
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")
        
        # Parse user context if provided
        user_context_model = None
        if context:
            try:
                context_data = json.loads(context)
                api_context = UserContext(**context_data)
                user_context_model = convert_api_context_to_model(api_context)
                print(f"Parsed user context: {user_context_model.to_dict()}")
            except Exception as e:
                print(f"WARNING: Failed to parse context: {e}")
                # Continue without context rather than failing
        
        # Analyze text using rule engine service
        print("Running rule analysis...")
        flags = rule_engine_service.analyze_text(extracted_text, user_context_model)
        print(f"Found {len(flags)} flags")
        
        # Calculate analytics using scoring service
        analytics = scoring_service.create_analytics(flags)
        print(f"Forensic score: {analytics.forensic_score}")
        
        # Create metadata
        processing_time = time.time() - start_time
        metadata = ReportMetadata(
            filename=file.filename,
            text_length=len(extracted_text),
            upload_timestamp=str(int(time.time())),
            processing_time=processing_time
        )
        
        # Create report
        report = Report(
            id=report_id,
            status="completed",
            flags=flags,
            analytics=analytics,
            metadata=metadata
        )
        
        # Store report (convert to dict for compatibility with original format)
        reports_store[report_id] = report.to_dict()
        
        print(f"Report {report_id} created successfully in {processing_time:.2f}s")
        return {"report_id": report_id}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR processing file: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")


@app.get("/report/{report_id}")
async def get_report(report_id: str):
    """Get analysis report by ID."""
    
    # Validate report ID
    validation_result = validation_service.validate_report_id(report_id)
    if not validation_result['valid']:
        raise HTTPException(status_code=400, detail=validation_result['errors'][0])
    
    if report_id not in reports_store:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return JSONResponse(content=reports_store[report_id])


@app.get("/reports")
async def list_reports():
    """List all reports (admin endpoint)."""
    return {
        "reports": list(reports_store.keys()),
        "count": len(reports_store)
    }


@app.delete("/report/{report_id}")
async def delete_report(report_id: str):
    """Delete a report."""
    
    # Validate report ID
    validation_result = validation_service.validate_report_id(report_id)
    if not validation_result['valid']:
        raise HTTPException(status_code=400, detail=validation_result['errors'][0])
    
    if report_id not in reports_store:
        raise HTTPException(status_code=404, detail="Report not found")
    
    del reports_store[report_id]
    return {"message": "Report deleted successfully"}


# Development endpoints for debugging
@app.get("/debug/rules")
async def debug_rules():
    """Debug endpoint to inspect loaded rules."""
    if not rule_engine_service:
        raise HTTPException(status_code=500, detail="Rule engine not initialized")
    
    return {
        "rules_summary": rule_engine_service.get_rules_summary(),
        "validation": rule_engine_service.validate_rules_config()
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)