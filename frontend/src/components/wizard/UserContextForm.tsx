/**
 * User context form component for capturing user expectations and promises
 */

import React from 'react';
import { UserContext } from '@/types';
import { Card, Button } from '@/components/ui';

interface UserContextFormProps {
  userContext: UserContext;
  onUpdateContext: (updates: Partial<UserContext>) => void;
  onSubmit: () => void;
}

export const UserContextForm: React.FC<UserContextFormProps> = ({
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

  return (
    <div className="animate-in slide-in-from-left duration-300">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-slate-900 mb-3">Tell us about your situation</h2>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
          Help us catch any deceptions by sharing what you were promised and expected.
        </p>
      </div>

      <div className="grid gap-8">
        {/* Purchase Details Card */}
        <Card gradient="blue">
          <h3 className="text-xl font-semibold text-slate-900 mb-4 flex items-center">
            <svg className="w-5 h-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
            </svg>
            Purchase Details
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Expected Purchase Price
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-slate-500 text-sm">$</span>
                </div>
                <input
                  type="number"
                  value={userContext.expectedPurchasePrice || ''}
                  onChange={(e) => handleNumberChange('expectedPurchasePrice', e.target.value)}
                  className="block w-full pl-7 pr-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors text-slate-900 bg-white"
                  placeholder="400000"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Expected Loan Amount
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-slate-500 text-sm">$</span>
                </div>
                <input
                  type="number"
                  value={userContext.expectedLoanAmount || ''}
                  onChange={(e) => handleNumberChange('expectedLoanAmount', e.target.value)}
                  className="block w-full pl-7 pr-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors text-slate-900 bg-white"
                  placeholder="320000"
                />
              </div>
            </div>
          </div>
        </Card>

        {/* Loan Type Card */}
        <Card gradient="slate">
          <label className="block text-xl font-semibold text-slate-900 mb-4 flex items-center">
            <svg className="w-5 h-5 text-slate-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v6a2 2 0 002 2h2m0 0h2m-2 0v4l3-3m-3 3l-3-3" />
            </svg>
            What type of loan were you expecting?
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {loanTypes.map((type) => (
              <label key={type} className={`relative flex items-center justify-center p-4 rounded-lg border-2 cursor-pointer transition-all hover:shadow-md ${
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

        {/* Builder Promises Card */}
        <Card gradient="green">
          <h3 className="text-xl font-semibold text-slate-900 mb-4 flex items-center">
            <svg className="w-5 h-5 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            What did your builder/lender promise?
          </h3>
          <div className="space-y-4">
            <div className="flex items-center">
              <input
                id="zero-closing-costs"
                type="checkbox"
                checked={userContext.promisedZeroClosingCosts}
                onChange={(e) => onUpdateContext({ promisedZeroClosingCosts: e.target.checked })}
                className="w-4 h-4 text-green-600 bg-gray-100 border-slate-300 rounded focus:ring-green-500 focus:ring-2"
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
                className="w-4 h-4 text-green-600 bg-gray-100 border-slate-300 rounded focus:ring-green-500 focus:ring-2"
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
                className="w-4 h-4 text-green-600 bg-gray-100 border-slate-300 rounded focus:ring-green-500 focus:ring-2"
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
                className="w-4 h-4 text-green-600 bg-gray-100 border-slate-300 rounded focus:ring-green-500 focus:ring-2"
              />
              <label htmlFor="buyer-agent" className="ml-3 text-sm font-medium text-slate-700">
                Had buyer's agent representation
              </label>
            </div>
          </div>
        </Card>

        <div className="mt-8">
          <Button
            onClick={onSubmit}
            variant="primary"
            size="lg"
            className="w-full"
          >
            Continue to Upload
          </Button>
        </div>
      </div>
    </div>
  );
};