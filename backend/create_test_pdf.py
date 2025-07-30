from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def create_test_pdf():
    """Create a test PDF with content that will trigger our CloseGuard rules."""
    
    filename = "test_closing_document.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Create content that will trigger multiple rules
    content = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("HOME CLOSING DISCLOSURE STATEMENT", styles['Title'])
    content.append(title)
    content.append(Spacer(1, 20))
    
    # Content that will trigger "high_closing_costs" rule (>$5,000)
    closing_costs = Paragraph("Total Closing Costs: $7,850.00", styles['Normal'])
    content.append(closing_costs)
    content.append(Spacer(1, 12))
    
    # Content that will trigger "excessive_loan_amount" rule (>$500,000)
    loan_amount = Paragraph("Principal Loan Amount: $750,000.00", styles['Normal'])
    content.append(loan_amount)
    content.append(Spacer(1, 12))
    
    # Content that will trigger "high_interest_rate" rule (>7%)
    interest_rate = Paragraph("Interest Rate (APR): 8.25%", styles['Normal'])
    content.append(interest_rate)
    content.append(Spacer(1, 12))
    
    # Content that will trigger "suspicious_wire_transfer" rule (>$10,000)
    wire_transfer = Paragraph("Wire Transfer for Down Payment: $15,000.00", styles['Normal'])
    content.append(wire_transfer)
    content.append(Spacer(1, 12))
    
    # Add some normal content
    normal_content = [
        "Property Address: 123 Main Street, Anytown, ST 12345",
        "Borrower: John and Jane Doe",
        "Lender: ABC Mortgage Company",
        "",
        "LOAN DETAILS:",
        "Loan Term: 30 years",
        "Monthly Payment: $4,987.23",
        "",
        "FEES AND CHARGES:",
        "Origination Fee: $2,500.00",
        "Appraisal Fee: $650.00",
        "Credit Report Fee: $75.00",
        "Recording Fee: $125.00",
        "",
        "THIRD PARTY SERVICES:",
        "Attorney Fee: $1,200.00",
        "",
        "Note: This document contains important information about your mortgage loan.",
        "Please review all terms and conditions carefully before signing."
    ]
    
    for text in normal_content:
        if text:
            p = Paragraph(text, styles['Normal'])
            content.append(p)
            content.append(Spacer(1, 8))
        else:
            content.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(content)
    print(f"Test PDF created: {filename}")
    return filename


if __name__ == "__main__":
    create_test_pdf()