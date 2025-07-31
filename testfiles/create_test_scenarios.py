from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import os


def create_builder_broken_promises_pdf():
    """
    Scenario 1: Builder Broken Promises
    - Builder promised to pay $3,000 in closing costs but buyer pays them
    - Missing buyer agent representation
    - Should trigger multiple red flags
    """
    filename = "testfiles/scenario_1_builder_broken_promises.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter, 
                          rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    content = []
    styles = getSampleStyleSheet()
    
    # Header
    title = Paragraph("CLOSING DISCLOSURE", styles['Title'])
    content.append(title)
    content.append(Spacer(1, 12))
    
    subtitle = Paragraph("This form is a statement of final loan terms and closing costs. Compare this document with your Loan Estimate.", styles['Normal'])
    content.append(subtitle)
    content.append(Spacer(1, 20))
    
    # Transaction Information
    content.append(Paragraph("Transaction Information", styles['Heading2']))
    content.append(Spacer(1, 12))
    
    transaction_data = [
        ["Borrower", "John Smith and Jane Smith", "Lender", "Texas Home Bank"],
        ["", "456 Test Street", "", ""],
        ["", "Austin, TX 78701", "", ""],
        ["", "", "", ""],
        ["Seller", "ABC Builder Corporation", "Loan Information", ""],
        ["", "1234 Builder Drive", "Loan Term", "30 years"],
        ["", "Dallas, TX 75201", "Purpose", "Purchase"],
        ["", "", "Product", "Fixed Rate"],
        ["", "", "Loan Type", "☒ Conventional ☐ FHA ☐ VA"],
        ["", "", "Loan ID #", "TEST123456"]
    ]
    
    t = Table(transaction_data, colWidths=[1.5*inch, 3*inch, 1.5*inch, 2*inch])
    t.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]))
    content.append(t)
    content.append(Spacer(1, 20))
    
    # Loan Terms
    content.append(Paragraph("Loan Terms", styles['Heading2']))
    content.append(Spacer(1, 12))
    
    loan_data = [
        ["Loan Amount", "$285,000", "Can this amount increase after closing?"],
        ["", "", "NO"],
        ["Interest Rate", "7.875%", "NO"],
        ["Monthly Principal & Interest", "$2,098.45", "NO"]
    ]
    
    t2 = Table(loan_data, colWidths=[2*inch, 1.5*inch, 3*inch])
    t2.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]))
    content.append(t2)
    content.append(Spacer(1, 20))
    
    # Costs at Closing - This is where the broken promise shows up
    content.append(Paragraph("Costs at Closing", styles['Heading2']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("Closing Costs: $12,847.50", styles['Normal']))
    content.append(Paragraph("Cash to Close: $68,247.50", styles['Normal']))
    content.append(Spacer(1, 20))
    
    # Detailed Closing Costs - Page 2 simulation
    content.append(Paragraph("Closing Cost Details", styles['Heading2']))
    content.append(Spacer(1, 12))
    
    # Loan Costs
    content.append(Paragraph("A. Origination Charges: $4,275.00", styles['Normal']))
    content.append(Paragraph("   - Origination Fee (1.5% of loan amount): $4,275.00", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("B. Services Borrower Did Not Shop For: $1,250.00", styles['Normal']))
    content.append(Paragraph("   - Appraisal Fee: $650.00", styles['Normal']))
    content.append(Paragraph("   - Credit Report Fee: $45.00", styles['Normal']))
    content.append(Paragraph("   - Flood Certification: $35.00", styles['Normal']))
    content.append(Paragraph("   - Tax Service Fee: $520.00", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("C. Services Borrower Did Shop For: $2,850.00", styles['Normal']))
    content.append(Paragraph("   - Title Insurance: $1,200.00", styles['Normal']))
    content.append(Paragraph("   - Settlement Fee: $750.00", styles['Normal']))
    content.append(Paragraph("   - Survey Fee: $450.00", styles['Normal']))
    content.append(Paragraph("   - Home Inspection: $450.00", styles['Normal']))
    content.append(Spacer(1, 12))
    
    # THE KEY ISSUE - Builder was supposed to pay these but buyer is paying
    content.append(Paragraph("H. Other Costs: $4,472.50", styles['Heading3']))
    content.append(Paragraph("   - Builder Closing Cost Credit: $0.00 (PROMISED: $3,000)", styles['Normal']))
    content.append(Paragraph("   - Recording Fees (Buyer Paying): $125.00", styles['Normal']))
    content.append(Paragraph("   - Transfer Tax (Buyer Paying): $1,425.00", styles['Normal']))
    content.append(Paragraph("   - HOA Setup Fee (Buyer Paying): $350.00", styles['Normal']))
    content.append(Paragraph("   - Warranty Fee (Buyer Paying): $750.00", styles['Normal']))
    content.append(Paragraph("   - Additional Title Fees (Buyer Paying): $1,822.50", styles['Normal']))
    content.append(Spacer(1, 12))
    
    # Real Estate Agents - MISSING BUYER AGENT
    content.append(Paragraph("Real Estate Commissions", styles['Heading3']))
    content.append(Paragraph("   - Real Estate Commission to ABC Realty (Seller Agent): $17,100.00", styles['Normal']))
    content.append(Paragraph("   - Buyer Agent Commission: NOT LISTED", styles['Normal']))
    content.append(Spacer(1, 12))
    
    # Summary showing the problem
    content.append(Paragraph("SUMMARY OF ISSUES:", styles['Heading2']))
    content.append(Paragraph("1. Builder ABC Corporation promised $3,000 closing cost credit - NOT PROVIDED", styles['Normal']))
    content.append(Paragraph("2. Buyer paying fees typically paid by seller/builder", styles['Normal']))
    content.append(Paragraph("3. No buyer agent representation identified", styles['Normal']))
    content.append(Paragraph("4. Excessive origination fee: 1.5% ($4,275) vs typical 1.0%", styles['Normal']))
    
    # Build the PDF
    doc.build(content)
    print(f"Created: {filename}")
    return filename


def create_excessive_fees_pdf():
    """
    Scenario 2: Excessive Fees
    - High origination fees (2% instead of typical 1%)
    - Inflated title/settlement costs
    - Unnecessary junk fees
    """
    filename = "testfiles/scenario_2_excessive_fees.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                          rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    content = []
    styles = getSampleStyleSheet()
    
    # Header
    title = Paragraph("CLOSING DISCLOSURE", styles['Title'])
    content.append(title)
    content.append(Spacer(1, 12))
    
    subtitle = Paragraph("This form is a statement of final loan terms and closing costs.", styles['Normal'])
    content.append(subtitle)
    content.append(Spacer(1, 20))
    
    # Transaction Information
    content.append(Paragraph("Transaction Information", styles['Heading2']))
    content.append(Paragraph("Borrower: Michael Rodriguez and Maria Rodriguez", styles['Normal']))
    content.append(Paragraph("Property: 789 Oak Lane, Houston, TX 77001", styles['Normal']))
    content.append(Paragraph("Sale Price: $425,000", styles['Normal']))
    content.append(Paragraph("Loan Amount: $340,000", styles['Normal']))
    content.append(Spacer(1, 20))
    
    # The Problem - Excessive Fees
    content.append(Paragraph("CLOSING COSTS BREAKDOWN", styles['Heading2']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("A. ORIGINATION CHARGES: $8,500.00", styles['Heading3']))
    content.append(Paragraph("   - Origination Fee (2.5% of loan): $8,500.00 ⚠️ EXCESSIVE", styles['Normal']))
    content.append(Paragraph("   - Typical range: 0.5-1.0% ($1,700-$3,400)", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("B. LENDER FEES: $2,850.00", styles['Heading3']))
    content.append(Paragraph("   - Processing Fee: $895.00 ⚠️ HIGH", styles['Normal']))
    content.append(Paragraph("   - Underwriting Fee: $1,200.00 ⚠️ HIGH", styles['Normal']))
    content.append(Paragraph("   - Application Fee: $500.00", styles['Normal']))
    content.append(Paragraph("   - Document Preparation: $255.00", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("C. TITLE AND SETTLEMENT: $4,250.00", styles['Heading3']))
    content.append(Paragraph("   - Title Insurance: $1,800.00 ⚠️ HIGH", styles['Normal']))
    content.append(Paragraph("   - Settlement Fee: $1,250.00 ⚠️ HIGH", styles['Normal']))
    content.append(Paragraph("   - Title Search: $650.00", styles['Normal']))
    content.append(Paragraph("   - Document Recording: $350.00", styles['Normal']))
    content.append(Paragraph("   - Notary Fee: $200.00", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("D. JUNK FEES: $1,485.00", styles['Heading3']))
    content.append(Paragraph("   - Administrative Fee: $395.00", styles['Normal']))
    content.append(Paragraph("   - File Management Fee: $275.00", styles['Normal']))
    content.append(Paragraph("   - Courier Fee: $185.00", styles['Normal']))
    content.append(Paragraph("   - Document Review Fee: $325.00", styles['Normal']))
    content.append(Paragraph("   - Compliance Fee: $305.00", styles['Normal']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("TOTAL EXCESSIVE FEES: $17,085.00", styles['Heading2']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("MARKET COMPARISON:", styles['Heading3']))
    content.append(Paragraph("• Typical total lender fees: $3,000-$5,000", styles['Normal']))
    content.append(Paragraph("• Your total lender fees: $11,350.00", styles['Normal']))
    content.append(Paragraph("• OVERAGE: $6,350-$8,350", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("• Typical title/settlement: $1,500-$2,500", styles['Normal']))
    content.append(Paragraph("• Your title/settlement: $4,250.00", styles['Normal']))
    content.append(Paragraph("• OVERAGE: $1,750-$2,750", styles['Normal']))
    
    # Build the PDF
    doc.build(content)
    print(f"Created: {filename}")
    return filename


def create_fee_allocation_issues_pdf():
    """
    Scenario 3: Fee Allocation Issues
    - Title insurance charged to buyer (should be seller)
    - Warranty fees buyer is paying
    - Recording fees improperly allocated
    """
    filename = "testfiles/scenario_3_fee_allocation_issues.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                          rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    content = []
    styles = getSampleStyleSheet()
    
    # Header
    title = Paragraph("CLOSING DISCLOSURE", styles['Title'])
    content.append(title)
    content.append(Spacer(1, 20))
    
    content.append(Paragraph("Transaction Information", styles['Heading2']))
    content.append(Paragraph("Borrower: David Kim and Sarah Kim", styles['Normal']))
    content.append(Paragraph("Property: 321 Pine Street, San Antonio, TX 78201", styles['Normal']))
    content.append(Paragraph("Sale Price: $295,000", styles['Normal']))
    content.append(Spacer(1, 20))
    
    # The main issue - improper fee allocation
    content.append(Paragraph("CLOSING COST ALLOCATION ISSUES", styles['Heading2']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("BUYER-PAID COSTS (Issues Highlighted):", styles['Heading3']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("Title and Insurance Costs:", styles['Normal']))
    content.append(Paragraph("• Owner's Title Insurance: $1,650.00 ⚠️ SHOULD BE SELLER-PAID", styles['Normal']))
    content.append(Paragraph("• Lender's Title Insurance: $850.00 ✓ Correctly buyer-paid", styles['Normal']))
    content.append(Paragraph("• Title Search Fee: $450.00 ⚠️ TYPICALLY SELLER-PAID", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("Recording and Transfer Costs:", styles['Normal']))
    content.append(Paragraph("• Deed Recording Fee: $125.00 ⚠️ SHOULD BE SELLER-PAID", styles['Normal']))
    content.append(Paragraph("• Mortgage Recording Fee: $75.00 ✓ Correctly buyer-paid", styles['Normal']))
    content.append(Paragraph("• Transfer Tax: $1,475.00 ⚠️ TYPICALLY SELLER-PAID", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("Warranty and Protection:", styles['Normal']))
    content.append(Paragraph("• Home Warranty Premium: $595.00 ⚠️ SHOULD BE SELLER-PAID", styles['Normal']))
    content.append(Paragraph("• Termite Inspection: $125.00 ⚠️ TYPICALLY SELLER-PAID", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("Survey and Inspections:", styles['Normal']))
    content.append(Paragraph("• Property Survey: $525.00 ✓ Correctly buyer-paid", styles['Normal']))
    content.append(Paragraph("• Home Inspection: $450.00 ✓ Correctly buyer-paid", styles['Normal']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("SELLER-PAID COSTS:", styles['Heading3']))
    content.append(Paragraph("• Real Estate Commission: $17,700.00 ✓", styles['Normal']))
    content.append(Paragraph("• Attorney Fee: $750.00 ✓", styles['Normal']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("ANALYSIS:", styles['Heading2']))
    content.append(Paragraph("Improperly Allocated to Buyer: $4,445.00", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("Items that should typically be seller-paid:", styles['Normal']))
    content.append(Paragraph("1. Owner's Title Insurance: $1,650.00", styles['Normal']))
    content.append(Paragraph("2. Title Search Fee: $450.00", styles['Normal']))
    content.append(Paragraph("3. Deed Recording Fee: $125.00", styles['Normal']))
    content.append(Paragraph("4. Transfer Tax: $1,475.00", styles['Normal']))
    content.append(Paragraph("5. Home Warranty: $595.00", styles['Normal']))
    content.append(Paragraph("6. Termite Inspection: $125.00", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("RECOMMENDATION:", styles['Heading3']))
    content.append(Paragraph("Review your purchase contract to confirm fee allocation agreements.", styles['Normal']))
    content.append(Paragraph("These costs may have been improperly shifted to the buyer.", styles['Normal']))
    
    # Build the PDF
    doc.build(content)
    print(f"Created: {filename}")
    return filename


def create_clean_document_pdf():
    """
    Scenario 4: Clean Document (Control)
    - All fees within normal ranges
    - Proper fee allocation
    - Buyer agent present
    - No red flags
    """
    filename = "testfiles/scenario_4_clean_document.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                          rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    content = []
    styles = getSampleStyleSheet()
    
    # Header
    title = Paragraph("CLOSING DISCLOSURE", styles['Title'])
    content.append(title)
    content.append(Spacer(1, 20))
    
    content.append(Paragraph("Transaction Information", styles['Heading2']))
    content.append(Paragraph("Borrower: Jennifer Brown and Robert Brown", styles['Normal']))
    content.append(Paragraph("Property: 456 Maple Avenue, Austin, TX 78704", styles['Normal']))
    content.append(Paragraph("Sale Price: $350,000", styles['Normal']))
    content.append(Paragraph("Loan Amount: $280,000", styles['Normal']))
    content.append(Spacer(1, 20))
    
    content.append(Paragraph("CLOSING COSTS - ALL WITHIN NORMAL RANGES", styles['Heading2']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("A. Origination Charges: $2,800.00", styles['Heading3']))
    content.append(Paragraph("   - Origination Fee (1.0% of loan): $2,800.00 ✓ Normal", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("B. Lender Services: $825.00", styles['Heading3']))
    content.append(Paragraph("   - Appraisal Fee: $550.00 ✓", styles['Normal']))
    content.append(Paragraph("   - Credit Report: $45.00 ✓", styles['Normal']))
    content.append(Paragraph("   - Flood Certification: $35.00 ✓", styles['Normal']))
    content.append(Paragraph("   - Tax Service: $95.00 ✓", styles['Normal']))
    content.append(Paragraph("   - Processing Fee: $100.00 ✓", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("C. Title and Settlement: $1,950.00", styles['Heading3']))
    content.append(Paragraph("   - Lender's Title Insurance: $750.00 ✓ Buyer pays", styles['Normal']))
    content.append(Paragraph("   - Settlement Fee: $650.00 ✓ Normal", styles['Normal']))
    content.append(Paragraph("   - Title Search: $350.00 ✓ Normal", styles['Normal']))
    content.append(Paragraph("   - Mortgage Recording: $85.00 ✓ Buyer pays", styles['Normal']))
    content.append(Paragraph("   - Notary: $115.00 ✓", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("D. Third Party Services: $1,125.00", styles['Heading3']))
    content.append(Paragraph("   - Home Inspection: $475.00 ✓ Buyer pays", styles['Normal']))
    content.append(Paragraph("   - Survey: $425.00 ✓ Buyer pays", styles['Normal']))
    content.append(Paragraph("   - Pest Inspection: $125.00 ✓", styles['Normal']))
    content.append(Paragraph("   - HOA Transfer Fee: $100.00 ✓", styles['Normal']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("SELLER-PAID COSTS (Properly Allocated):", styles['Heading3']))
    content.append(Paragraph("• Owner's Title Insurance: $1,200.00 ✓ Seller pays", styles['Normal']))
    content.append(Paragraph("• Transfer Tax: $1,750.00 ✓ Seller pays", styles['Normal']))
    content.append(Paragraph("• Deed Recording: $125.00 ✓ Seller pays", styles['Normal']))
    content.append(Paragraph("• Home Warranty: $525.00 ✓ Seller pays", styles['Normal']))
    content.append(Paragraph("• Real Estate Commission: $21,000.00 ✓ Seller pays", styles['Normal']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("REAL ESTATE REPRESENTATION:", styles['Heading3']))
    content.append(Paragraph("• Buyer Agent: ABC Realty - Sarah Johnson ✓", styles['Normal']))
    content.append(Paragraph("• Seller Agent: XYZ Properties - Mike Davis ✓", styles['Normal']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("TOTAL BUYER CLOSING COSTS: $6,700.00", styles['Heading2']))
    content.append(Paragraph("This is within the normal range of $5,000-$8,000 for this loan amount.", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("✓ NO ISSUES IDENTIFIED", styles['Heading2']))
    content.append(Paragraph("All fees are within normal ranges and properly allocated.", styles['Normal']))
    
    # Build the PDF
    doc.build(content)
    print(f"Created: {filename}")
    return filename


def create_missing_representation_pdf():
    """
    Scenario 5: Missing Buyer Representation
    - No buyer agent listed anywhere
    - Only seller agent present
    - Potential representation issues
    """
    filename = "testfiles/scenario_5_missing_representation.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                          rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    content = []
    styles = getSampleStyleSheet()
    
    # Header
    title = Paragraph("CLOSING DISCLOSURE", styles['Title'])
    content.append(title)
    content.append(Spacer(1, 20))
    
    content.append(Paragraph("Transaction Information", styles['Heading2']))
    content.append(Paragraph("Borrower: Lisa Martinez", styles['Normal']))
    content.append(Paragraph("Property: 159 Cedar Road, Plano, TX 75023", styles['Normal']))
    content.append(Paragraph("Sale Price: $275,000", styles['Normal']))
    content.append(Paragraph("Seller: Highland Homes (Builder)", styles['Normal']))
    content.append(Spacer(1, 20))
    
    content.append(Paragraph("REAL ESTATE REPRESENTATION ANALYSIS", styles['Heading2']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("⚠️ BUYER REPRESENTATION ISSUE IDENTIFIED", styles['Heading3']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("Seller Representation:", styles['Normal']))
    content.append(Paragraph("• Listing Agent: Highland Sales - Tom Wilson", styles['Normal']))
    content.append(Paragraph("• Seller Agent Commission: $16,500.00", styles['Normal']))
    content.append(Paragraph("• License #: TX-123456", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("Buyer Representation:", styles['Normal']))
    content.append(Paragraph("• Buyer Agent: NOT LISTED ⚠️", styles['Normal']))
    content.append(Paragraph("• Buyer Agent Commission: $0.00 ⚠️", styles['Normal']))
    content.append(Paragraph("• Buyer Agent License: NOT PROVIDED ⚠️", styles['Normal']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("CLOSING COSTS", styles['Heading2']))
    content.append(Paragraph("Total Closing Costs: $8,750.00", styles['Normal']))
    content.append(Paragraph("• Processing Fee: $450.00", styles['Normal']))
    content.append(Paragraph("• Origination Fee: $2,750.00", styles['Normal']))
    content.append(Paragraph("• Title Insurance: $1,200.00", styles['Normal']))
    content.append(Paragraph("• Settlement Fee: $650.00", styles['Normal']))
    content.append(Paragraph("• Recording Fees: $175.00", styles['Normal']))
    content.append(Paragraph("• Other Fees: $3,525.00", styles['Normal']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("POTENTIAL ISSUES:", styles['Heading2']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("1. NO BUYER REPRESENTATION", styles['Heading3']))
    content.append(Paragraph("   • No licensed agent protecting buyer interests", styles['Normal']))
    content.append(Paragraph("   • Seller agent represents seller/builder only", styles['Normal']))
    content.append(Paragraph("   • Potential conflict of interest", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("2. UNEQUAL REPRESENTATION", styles['Heading3']))
    content.append(Paragraph("   • Seller has professional representation", styles['Normal']))
    content.append(Paragraph("   • Buyer navigating complex transaction alone", styles['Normal']))
    content.append(Paragraph("   • No advocate for buyer contract terms", styles['Normal']))
    content.append(Spacer(1, 8))
    
    content.append(Paragraph("3. COMMISSION STRUCTURE", styles['Heading3']))
    content.append(Paragraph("   • Total commission: $16,500 (6.0%)", styles['Normal']))
    content.append(Paragraph("   • All commission going to seller side", styles['Normal']))
    content.append(Paragraph("   • No buyer agent to split commission", styles['Normal']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("RECOMMENDATIONS:", styles['Heading2']))
    content.append(Paragraph("• Verify if you have buyer representation agreement", styles['Normal']))
    content.append(Paragraph("• Consider consulting with a buyer's agent", styles['Normal']))
    content.append(Paragraph("• Review all contract terms carefully", styles['Normal']))
    content.append(Paragraph("• Ensure your interests are protected", styles['Normal']))
    
    # Build the PDF
    doc.build(content)
    print(f"Created: {filename}")
    return filename


if __name__ == "__main__":
    print("Creating test scenario PDFs...")
    
    # Create all test scenarios
    create_builder_broken_promises_pdf()
    create_excessive_fees_pdf()
    create_fee_allocation_issues_pdf()
    create_clean_document_pdf()
    create_missing_representation_pdf()
    
    print("\nAll test scenario PDFs created successfully!")