/**
 * Cost breakdown component for Texas-specific cost analysis
 */

import React from 'react';
import { Card } from '@/components/ui';

interface CostItem {
  name: string;
  description: string;
  paidBy: string;
  amount: number;
  typicalRange: string;
  isUnexpected: boolean;
  isExcessive: boolean;
}

interface CostBreakdownProps {
  report?: any; // Report object from the analysis
}

export const CostBreakdown: React.FC<CostBreakdownProps> = ({ report }) => {
  const generateCostBreakdown = (): CostItem[] => {
    if (!report) return [];
    
    // Mock cost breakdown based on typical closing disclosure items
    // In a real implementation, this would parse the actual document text
    return [
      {
        name: "Origination Fee",
        description: "Lender fee for processing loan",
        paidBy: "Borrower",
        amount: 2500,
        typicalRange: "$0-2,000",
        isUnexpected: false,
        isExcessive: true,
      },
      {
        name: "Title Insurance (Owner's)",
        description: "Protects owner from title defects",
        paidBy: "Borrower",
        amount: 1200,
        typicalRange: "$800-1,500",
        isUnexpected: true, // Should be paid by seller in TX
        isExcessive: false,
      },
      {
        name: "Title Insurance (Lender's)",
        description: "Protects lender from title defects",
        paidBy: "Borrower",
        amount: 600,
        typicalRange: "$400-800",
        isUnexpected: false,
        isExcessive: false,
      },
      {
        name: "Property Survey",
        description: "Legal boundary survey",
        paidBy: "Borrower",
        amount: 450,
        typicalRange: "$300-600",
        isUnexpected: true, // Should be paid by seller in TX new construction
        isExcessive: false,
      },
      {
        name: "Settlement/Closing Fee",
        description: "Title company closing service",
        paidBy: "Borrower",
        amount: 750,
        typicalRange: "$500-1,000",
        isUnexpected: true, // Often covered by builder
        isExcessive: false,
      },
      {
        name: "Document Preparation",
        description: "Preparing closing documents",
        paidBy: "Borrower",
        amount: 200,
        typicalRange: "$0-300",
        isUnexpected: true, // Typically lender/title company cost
        isExcessive: false,
      },
      {
        name: "Notary Fee",
        description: "Notarizing signatures",
        paidBy: "Borrower",
        amount: 75,
        typicalRange: "$0-100",
        isUnexpected: true, // Typically covered by title company
        isExcessive: false,
      },
      {
        name: "Appraisal Fee",
        description: "Property valuation",
        paidBy: "Borrower",
        amount: 550,
        typicalRange: "$450-650",
        isUnexpected: false,
        isExcessive: false,
      },
      {
        name: "Credit Report",
        description: "Borrower credit check",
        paidBy: "Borrower",
        amount: 45,
        typicalRange: "$25-75",
        isUnexpected: false,
        isExcessive: false,
      },
      {
        name: "Recording Fees",
        description: "County recording of deed/mortgage",
        paidBy: "Borrower",
        amount: 125,
        typicalRange: "$80-200",
        isUnexpected: false,
        isExcessive: false,
      }
    ];
  };

  const calculateTotalPaid = (payer: string): number => {
    return generateCostBreakdown()
      .filter(item => item.paidBy === payer)
      .reduce((total, item) => total + item.amount, 0);
  };

  const countUnexpectedCharges = (): number => {
    return generateCostBreakdown().filter(item => item.isUnexpected).length;
  };

  const costBreakdown = generateCostBreakdown();
  const borrowerTotal = calculateTotalPaid("Borrower");
  const sellerTotal = calculateTotalPaid("Seller");
  const unexpectedCount = countUnexpectedCharges();

  if (!report) {
    return null;
  }

  return (
    <Card className="shadow-lg border border-slate-200">
      <h3 className="text-xl font-bold text-slate-900 mb-4 flex items-center">
        <svg className="w-5 h-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
        </svg>
        Texas Cost Breakdown Analysis
      </h3>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-red-50 p-4 rounded-lg border border-red-200">
          <div className="text-2xl font-bold text-red-600">
            ${borrowerTotal.toLocaleString()}
          </div>
          <div className="text-sm font-medium text-red-700">Borrower Pays</div>
        </div>
        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
          <div className="text-2xl font-bold text-green-600">
            ${sellerTotal.toLocaleString()}
          </div>
          <div className="text-sm font-medium text-green-700">Seller Pays</div>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
          <div className="text-2xl font-bold text-yellow-600">
            {unexpectedCount}
          </div>
          <div className="text-sm font-medium text-yellow-700">Unexpected Charges</div>
        </div>
      </div>

      {/* Cost Items */}
      <div className="space-y-3">
        {costBreakdown.map((item, index) => (
          <div
            key={index}
            className={`p-4 rounded-lg border-2 ${
              item.isUnexpected 
                ? 'bg-yellow-50 border-yellow-200' 
                : item.isExcessive 
                  ? 'bg-red-50 border-red-200' 
                  : 'bg-slate-50 border-slate-200'
            }`}
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="font-semibold text-slate-900">{item.name}</h4>
                  {item.isUnexpected && (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                      Unexpected
                    </span>
                  )}
                  {item.isExcessive && (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                      Excessive
                    </span>
                  )}
                </div>
                <p className="text-sm text-slate-600 mb-2">{item.description}</p>
                <div className="text-xs text-slate-500">
                  Paid by: <span className="font-medium">{item.paidBy}</span> • 
                  Typical range: <span className="font-medium">{item.typicalRange}</span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-lg font-bold text-slate-900">
                  ${item.amount.toLocaleString()}
                </div>
              </div>
            </div>
            
            {item.isUnexpected && (
              <div className="mt-3 p-3 bg-yellow-100 rounded border">
                <p className="text-sm text-yellow-800">
                  <strong>⚠️ In Texas:</strong> This fee is typically paid by the seller or builder, especially in new construction. 
                  You may want to question why this cost was shifted to you.
                </p>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Educational Content */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h4 className="font-semibold text-blue-900 mb-2">💡 Texas Market Knowledge</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Owner's title insurance is typically paid by the seller in Texas</li>
          <li>• Property surveys are usually seller responsibility in new construction</li>
          <li>• Many builders cover settlement/closing fees as buyer incentives</li>
          <li>• Document prep and notary fees are often included in title company services</li>
        </ul>
      </div>
    </Card>
  );
};