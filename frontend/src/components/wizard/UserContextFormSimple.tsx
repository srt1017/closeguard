/**
 * Simplified user context form with progressive disclosure
 */

import React, { useState } from 'react';
import { UserContext } from '@/types';
import { Card, Button, Tabs } from '@/components/ui';

interface UserContextFormSimpleProps {
  userContext: UserContext;
  onUpdateContext: (updates: Partial<UserContext>) => void;
  onSubmit: () => void;
}

export const UserContextFormSimple: React.FC<UserContextFormSimpleProps> = ({
  userContext,
  onUpdateContext,
  onSubmit
}) => {
  const handleNumberChange = (field: keyof UserContext, value: string) => {
    onUpdateContext({
      [field]: value ? Number(value) : undefined
    });
  };

  const loanTypes = ['FHA', 'Conventional', 'VA', 'USDA', 'Not sure'] as const;

  const isBasicComplete = userContext.expectedPurchasePrice && userContext.expectedLoanAmount && userContext.expectedLoanType;

  const tabs = [
    {
      id: 'basics',
      label: 'Basic Info',
      content: (
        <div className="space-y-6">
          {/* Essential Purchase Information */}
          <Card>
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Purchase Information</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Purchase Price *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <span className="text-slate-500 text-sm">$</span>
                  </div>
                  <input
                    type="number"
                    value={userContext.expectedPurchasePrice || ''}
                    onChange={(e) => handleNumberChange('expectedPurchasePrice', e.target.value)}
                    className="block w-full pl-7 pr-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="400000"
                    required
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Loan Amount *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <span className="text-slate-500 text-sm">$</span>
                  </div>
                  <input
                    type="number"
                    value={userContext.expectedLoanAmount || ''}
                    onChange={(e) => handleNumberChange('expectedLoanAmount', e.target.value)}
                    className="block w-full pl-7 pr-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="320000"
                    required
                  />
                </div>
              </div>
            </div>
          </Card>

          {/* Loan Type */}
          <Card>
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Loan Type *</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {loanTypes.map((type) => (
                <label key={type} className={`relative flex items-center justify-center p-4 rounded-lg border-2 cursor-pointer transition-all hover:shadow-sm ${
                  userContext.expectedLoanType === type 
                    ? 'border-blue-500 bg-blue-50 text-blue-700' 
                    : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300'
                }`}>
                  <input
                    type="radio"
                    name="loanType"
                    value={type}
                    checked={userContext.expectedLoanType === type}
                    onChange={(e) => onUpdateContext({ expectedLoanType: e.target.value as any })}
                    className="sr-only"
                  />
                  <span className="font-medium text-center">{type}</span>
                  {userContext.expectedLoanType === type && (
                    <div className="absolute top-2 right-2 w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center">
                      <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    </div>
                  )}
                </label>
              ))}
            </div>
          </Card>
        </div>
      )
    },
    {
      id: 'promises',
      label: 'Promises Made',
      content: (
        <div className="space-y-6">
          <Card>
            <h3 className="text-lg font-semibold text-slate-900 mb-4">What were you promised?</h3>
            <div className="space-y-4">
              <div className="flex items-center">
                <input
                  id="zero-closing-costs"
                  type="checkbox"
                  checked={userContext.promisedZeroClosingCosts}
                  onChange={(e) => onUpdateContext({ promisedZeroClosingCosts: e.target.checked })}
                  className="w-4 h-4 text-blue-600 bg-gray-100 border-slate-300 rounded focus:ring-blue-500 focus:ring-2"
                />
                <label htmlFor="zero-closing-costs" className="ml-3 text-sm font-medium text-slate-700">
                  Zero closing costs
                </label>
              </div>
              
              <div className="flex items-center">
                <input
                  id="used-preferred-lender"
                  type="checkbox"
                  checked={userContext.usedBuildersPreferredLender}
                  onChange={(e) => onUpdateContext({ usedBuildersPreferredLender: e.target.checked })}
                  className="w-4 h-4 text-blue-600 bg-gray-100 border-slate-300 rounded focus:ring-blue-500 focus:ring-2"
                />
                <label htmlFor="used-preferred-lender" className="ml-3 text-sm font-medium text-slate-700">
                  Used builder's preferred lender
                </label>
              </div>

              <div className="flex items-center">
                <input
                  id="title-fees"
                  type="checkbox"
                  checked={userContext.builderPromisedToCoverTitleFees}
                  onChange={(e) => onUpdateContext({ builderPromisedToCoverTitleFees: e.target.checked })}
                  className="w-4 h-4 text-blue-600 bg-gray-100 border-slate-300 rounded focus:ring-blue-500 focus:ring-2"
                />
                <label htmlFor="title-fees" className="ml-3 text-sm font-medium text-slate-700">
                  Builder promised to cover title fees
                </label>
              </div>

              <div className="flex items-center">
                <input
                  id="buyer-agent"
                  type="checkbox"
                  checked={userContext.hadBuyerAgent}
                  onChange={(e) => onUpdateContext({ hadBuyerAgent: e.target.checked })}
                  className="w-4 h-4 text-blue-600 bg-gray-100 border-slate-300 rounded focus:ring-blue-500 focus:ring-2"
                />
                <label htmlFor="buyer-agent" className="ml-3 text-sm font-medium text-slate-700">
                  Had buyer's agent representation
                </label>
              </div>
            </div>
          </Card>
        </div>
      )
    },
    {
      id: 'details',
      label: 'Additional Details',
      content: (
        <div className="space-y-6">
          <Card>
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Optional Details</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Expected Interest Rate (%)
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={userContext.expectedInterestRate || ''}
                  onChange={(e) => handleNumberChange('expectedInterestRate', e.target.value)}
                  className="block w-full px-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="6.5"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Builder Name
                </label>
                <input
                  type="text"
                  value={userContext.builderName || ''}
                  onChange={(e) => onUpdateContext({ builderName: e.target.value })}
                  className="block w-full px-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="e.g., LGI Homes, D.R. Horton, etc."
                />
              </div>
            </div>
            
            {userContext.hadBuyerAgent && (
              <div className="mt-4">
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Buyer's Agent Name
                </label>
                <input
                  type="text"
                  value={userContext.buyerAgentName || ''}
                  onChange={(e) => onUpdateContext({ buyerAgentName: e.target.value })}
                  className="block w-full px-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Your buyer's agent name"
                />
              </div>
            )}
          </Card>
        </div>
      )
    }
  ];

  return (
    <div className="animate-in slide-in-from-left duration-300">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-slate-900 mb-3">Tell us about your situation</h2>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
          We'll use this information to provide more accurate analysis of your closing documents.
        </p>
      </div>

      <Tabs tabs={tabs} defaultTab="basics" />

      <div className="mt-8 flex justify-between items-center">
        <div className="text-sm text-slate-500">
          {isBasicComplete ? (
            <span className="text-green-600 flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              Ready to continue
            </span>
          ) : (
            'Please complete the basic information to continue'
          )}
        </div>
        <Button
          onClick={onSubmit}
          disabled={!isBasicComplete}
          variant="primary"
          size="lg"
        >
          Continue to Upload
        </Button>
      </div>
    </div>
  );
};