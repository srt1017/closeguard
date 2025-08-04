#!/usr/bin/env python3

import sys
import os

# Add backend directory to path
backend_path = '/Users/omarfarooq/Desktop/Repositories/mortgagebuddy/backend'
sys.path.insert(0, backend_path)

# Import from our custom parser module
import parser as pdf_parser

def test_ocr_extraction():
    """Test OCR extraction on scanned PDFs"""
    
    test_files = [
        "/Users/omarfarooq/Desktop/Repositories/mortgagebuddy/testfiles/CD_14695MedDriveFrisco.pdf",
        "/Users/omarfarooq/Desktop/Repositories/mortgagebuddy/testfiles/CD_3501MeridianMcKinney.pdf"
    ]
    
    for pdf_path in test_files:
        print(f"\n{'='*80}")
        print(f"Testing OCR extraction for: {os.path.basename(pdf_path)}")
        print('='*80)
        
        # First, confirm regular extraction returns empty
        try:
            regular_text = pdf_parser.extract_text(pdf_path)
            print(f"Regular extraction returned {len(regular_text)} characters")
            if len(regular_text) > 0:
                print("Preview:", regular_text[:200])
            else:
                print("No text extracted with regular methods - proceeding with OCR")
        except Exception as e:
            print(f"Regular extraction failed: {e}")
        
        # Try OCR extraction
        try:
            print("\nAttempting OCR extraction...")
            ocr_text = pdf_parser.extract_text_ocr(pdf_path)
            print(f"OCR extraction successful! Extracted {len(ocr_text)} characters")
            
            # Show preview of extracted text
            if len(ocr_text) > 0:
                print("\nFirst 500 characters:")
                print("-" * 50)
                print(ocr_text[:500])
                print("-" * 50)
                
                # Look for key closing disclosure markers
                markers = [
                    "Closing Disclosure",
                    "Loan Amount",
                    "Interest Rate",
                    "Total Closing Costs",
                    "Borrower",
                    "Lender"
                ]
                
                found_markers = []
                for marker in markers:
                    if marker.lower() in ocr_text.lower():
                        found_markers.append(marker)
                
                print(f"\nFound {len(found_markers)}/{len(markers)} key closing disclosure markers:")
                for marker in found_markers:
                    print(f"  ✓ {marker}")
                
                if len(found_markers) >= 3:
                    print("✅ OCR extraction appears successful - document structure recognized")
                else:
                    print("⚠️  OCR extraction may be incomplete - few key markers found")
            else:
                print("❌ OCR extraction returned no text")
                
        except Exception as e:
            print(f"❌ OCR extraction failed: {e}")

if __name__ == "__main__":
    test_ocr_extraction()