'use client';

import { useState } from 'react';

interface Flag {
  rule: string;
  message: string;
  snippet: string;
}

interface Report {
  status: string;
  flags: Flag[];
  analytics?: {
    forensic_score: number;
    total_flags: number;
    high_severity: number;
    medium_severity: number;
    low_severity: number;
  };
  metadata?: {
    filename: string;
    text_length: number;
  };
}

interface UserContext {
  // Basic loan expectations
  expectedLoanType: 'FHA' | 'Conventional' | 'VA' | 'USDA' | 'Not sure';
  expectedInterestRate?: number;
  expectedClosingCosts?: number;
  
  // Purchase details
  expectedPurchasePrice?: number;
  expectedLoanAmount?: number;
  
  // Promises made by builder/lender
  promisedZeroClosingCosts: boolean;
  promisedLenderCredit?: number;
  promisedSellerCredit?: number;
  promisedRebate?: number;
  
  // Builder/lender relationships
  usedBuildersPreferredLender: boolean;
  builderName?: string;
  
  // Specific promises about fees
  builderPromisedToCoverTitleFees: boolean;
  builderPromisedToCoverEscrowFees: boolean;
  builderPromisedToCoverInspection: boolean;
  
  // Representation
  hadBuyerAgent: boolean;
  buyerAgentName?: string;
  
  // Mortgage insurance expectations
  expectedMortgageInsurance: boolean;
  expectedMortgageInsuranceAmount?: number;
}

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [report, setReport] = useState<Report | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState<'context' | 'upload' | 'results'>('context');
  const [userContext, setUserContext] = useState<UserContext>({
    expectedLoanType: 'Not sure',
    promisedZeroClosingCosts: false,
    usedBuildersPreferredLender: false,
    builderPromisedToCoverTitleFees: false,
    builderPromisedToCoverEscrowFees: false,
    builderPromisedToCoverInspection: false,
    hadBuyerAgent: false,
    expectedMortgageInsurance: false,
  });

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError(null);
    } else {
      setError('Please select a PDF file');
      setSelectedFile(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setError(null);
    setReport(null);

    try {
      // Upload PDF with context
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('context', JSON.stringify(userContext));

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
      
      const uploadResponse = await fetch(`${apiUrl}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!uploadResponse.ok) {
        throw new Error('Upload failed');
      }

      const uploadResult = await uploadResponse.json();
      const reportId = uploadResult.report_id;

      // Get report
      const reportResponse = await fetch(`${apiUrl}/report/${reportId}`);
      
      if (!reportResponse.ok) {
        throw new Error('Failed to get report');
      }

      const reportData = await reportResponse.json();
      setReport(reportData);
      setCurrentStep('results');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setUploading(false);
    }
  };

  const handleContextSubmit = () => {
    setCurrentStep('upload');
  };

  const handleBackToContext = () => {
    setCurrentStep('context');
    setReport(null);
    setSelectedFile(null);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.type === 'application/pdf') {
        setSelectedFile(file);
        setError(null);
      } else {
        setError('Please select a PDF file');
      }
    }
  };

  const getSeverityIcon = (message: string) => {
    if (message.includes('🚨') || message.includes('CRITICAL') || message.includes('ERROR') || message.includes('FRAUD')) {
      return '🚨';
    } else if (message.includes('⚠️') || message.includes('WARNING') || message.includes('DANGEROUS')) {
      return '⚠️';
    } else {
      return 'ℹ️';
    }
  };

  const getSeverityColor = (message: string) => {
    if (message.includes('🚨') || message.includes('CRITICAL') || message.includes('ERROR') || message.includes('FRAUD')) {
      return 'border-red-200 bg-red-50';
    } else if (message.includes('⚠️') || message.includes('WARNING') || message.includes('DANGEROUS')) {
      return 'border-amber-200 bg-amber-50';
    } else {
      return 'border-blue-200 bg-blue-50';
    }
  };

  const getSeverityTextColor = (message: string) => {
    if (message.includes('🚨') || message.includes('CRITICAL') || message.includes('ERROR') || message.includes('FRAUD')) {
      return 'text-red-900';
    } else if (message.includes('⚠️') || message.includes('WARNING') || message.includes('DANGEROUS')) {
      return 'text-amber-900';
    } else {
      return 'text-blue-900';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="max-w-5xl mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-r from-blue-600 to-blue-700 mb-6">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h1 className="text-5xl font-bold text-slate-900 mb-4">
            CloseGuard
          </h1>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            AI-powered protection against predatory lending and closing document fraud
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
          {/* Progress Indicator */}
          <div className="bg-gradient-to-r from-slate-50 to-slate-100 px-8 py-6 border-b border-slate-200">
            <div className="flex items-center justify-between max-w-md mx-auto">
              <div className="flex items-center">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all duration-300 ${
                  currentStep === 'context' 
                    ? 'bg-blue-600 text-white shadow-lg scale-110' 
                    : (currentStep === 'upload' || currentStep === 'results') 
                    ? 'bg-green-500 text-white' 
                    : 'bg-slate-200 text-slate-500'
                }`}>
                  {(currentStep === 'upload' || currentStep === 'results') ? '✓' : '1'}
                </div>
                <div className="ml-3">
                  <div className={`text-sm font-medium transition-colors ${
                    currentStep === 'context' ? 'text-blue-600' : 
                    (currentStep === 'upload' || currentStep === 'results') ? 'text-green-600' : 'text-slate-400'
                  }`}>Your Details</div>
                </div>
              </div>
              
              <div className={`w-16 h-0.5 transition-colors ${
                (currentStep === 'upload' || currentStep === 'results') ? 'bg-green-500' : 'bg-slate-200'
              }`}></div>
              
              <div className="flex items-center">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all duration-300 ${
                  currentStep === 'upload' 
                    ? 'bg-blue-600 text-white shadow-lg scale-110' 
                    : currentStep === 'results' 
                    ? 'bg-green-500 text-white' 
                    : 'bg-slate-200 text-slate-500'
                }`}>
                  {currentStep === 'results' ? '✓' : '2'}
                </div>
                <div className="ml-3">
                  <div className={`text-sm font-medium transition-colors ${
                    currentStep === 'upload' ? 'text-blue-600' : 
                    currentStep === 'results' ? 'text-green-600' : 'text-slate-400'
                  }`}>Upload & Analyze</div>
                </div>
              </div>
              
              <div className={`w-16 h-0.5 transition-colors ${
                currentStep === 'results' ? 'bg-green-500' : 'bg-slate-200'
              }`}></div>
              
              <div className="flex items-center">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all duration-300 ${
                  currentStep === 'results' 
                    ? 'bg-blue-600 text-white shadow-lg scale-110' 
                    : 'bg-slate-200 text-slate-500'
                }`}>
                  3
                </div>
                <div className="ml-3">
                  <div className={`text-sm font-medium transition-colors ${
                    currentStep === 'results' ? 'text-blue-600' : 'text-slate-400'
                  }`}>Results</div>
                </div>
              </div>
            </div>
          </div>

          <div className="p-8">
            {/* Context Form */}
            {currentStep === 'context' && (
              <div className="animate-in slide-in-from-left duration-300">
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-bold text-slate-900 mb-3">Tell us about your situation</h2>
                  <p className="text-lg text-slate-600 max-w-2xl mx-auto">Help us catch any deceptions by sharing what you were promised and expected.</p>
                </div>

                <div className="grid gap-8">
                  {/* Purchase Details Card */}
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
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
                            onChange={(e) => setUserContext({...userContext, expectedPurchasePrice: e.target.value ? Number(e.target.value) : undefined})}
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
                            onChange={(e) => setUserContext({...userContext, expectedLoanAmount: e.target.value ? Number(e.target.value) : undefined})}
                            className="block w-full pl-7 pr-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors text-slate-900 bg-white"
                            placeholder="320000"
                          />
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Loan Type Card */}
                  <div className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-xl p-6 border border-slate-200">
                    <label className="block text-xl font-semibold text-slate-900 mb-4 flex items-center">
                      <svg className="w-5 h-5 text-slate-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v6a2 2 0 002 2h2m0 0h2m-2 0v4l3-3m-3 3l-3-3" />
                      </svg>
                      What type of loan were you expecting?
                    </label>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                      {(['FHA', 'Conventional', 'VA', 'USDA', 'Not sure'] as const).map((type) => (
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
                            onChange={(e) => setUserContext({...userContext, expectedLoanType: e.target.value as any})}
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
                  </div>

                  {/* Cost Promises Card */}
                  <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl p-6 border border-amber-100">
                    <label className="block text-xl font-semibold text-slate-900 mb-4 flex items-center">
                      <svg className="w-5 h-5 text-amber-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                      </svg>
                      Were you promised any of the following?
                    </label>
                    <div className="space-y-4">
                      <label className={`flex items-center p-4 rounded-lg border cursor-pointer transition-all hover:shadow-sm ${
                        userContext.promisedZeroClosingCosts 
                          ? 'border-amber-300 bg-amber-50' 
                          : 'border-slate-200 bg-white hover:border-slate-300'
                      }`}>
                        <input
                          type="checkbox"
                          checked={userContext.promisedZeroClosingCosts}
                          onChange={(e) => setUserContext({...userContext, promisedZeroClosingCosts: e.target.checked})}
                          className="w-5 h-5 text-amber-600 border-slate-300 rounded focus:ring-amber-500 focus:ring-2"
                        />
                        <span className="ml-3 font-medium text-slate-800">Zero closing costs</span>
                      </label>
                      
                      <div className="bg-white rounded-lg p-4 border border-slate-200">
                        <h4 className="font-medium text-slate-800 mb-3">Promised amounts (if any):</h4>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                          <div>
                            <label className="block text-sm text-slate-600 mb-1">Lender credit</label>
                            <div className="relative">
                              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <span className="text-slate-400 text-sm">$</span>
                              </div>
                              <input
                                type="number"
                                value={userContext.promisedLenderCredit || ''}
                                onChange={(e) => setUserContext({...userContext, promisedLenderCredit: e.target.value ? Number(e.target.value) : undefined})}
                                className="block w-full pl-7 pr-3 py-2 border border-slate-300 rounded-md focus:ring-1 focus:ring-amber-500 focus:border-amber-500 text-sm text-slate-900 bg-white"
                                placeholder="0"
                              />
                            </div>
                          </div>
                          <div>
                            <label className="block text-sm text-slate-600 mb-1">Seller credit</label>
                            <div className="relative">
                              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <span className="text-slate-400 text-sm">$</span>
                              </div>
                              <input
                                type="number"
                                value={userContext.promisedSellerCredit || ''}
                                onChange={(e) => setUserContext({...userContext, promisedSellerCredit: e.target.value ? Number(e.target.value) : undefined})}
                                className="block w-full pl-7 pr-3 py-2 border border-slate-300 rounded-md focus:ring-1 focus:ring-amber-500 focus:border-amber-500 text-sm text-slate-900 bg-white"
                                placeholder="0"
                              />
                            </div>
                          </div>
                          <div>
                            <label className="block text-sm text-slate-600 mb-1">Builder rebate</label>
                            <div className="relative">
                              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <span className="text-slate-400 text-sm">$</span>
                              </div>
                              <input
                                type="number"
                                value={userContext.promisedRebate || ''}
                                onChange={(e) => setUserContext({...userContext, promisedRebate: e.target.value ? Number(e.target.value) : undefined})}
                                className="block w-full pl-7 pr-3 py-2 border border-slate-300 rounded-md focus:ring-1 focus:ring-amber-500 focus:border-amber-500 text-sm text-slate-900 bg-white"
                                placeholder="0"
                              />
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Builder Relationship Card */}
                  <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-6 border border-green-100">
                    <label className="block text-xl font-semibold text-slate-900 mb-4 flex items-center">
                      <svg className="w-5 h-5 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                      </svg>
                      Did you use the builder's preferred lender?
                    </label>
                    <div className="grid grid-cols-2 gap-3 mb-4">
                      <label className={`flex items-center justify-center p-4 rounded-lg border-2 cursor-pointer transition-all hover:shadow-md ${
                        userContext.usedBuildersPreferredLender 
                          ? 'border-green-500 bg-green-50 text-green-700' 
                          : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300'
                      }`}>
                        <input
                          type="radio"
                          name="builderLender"
                          value="yes"
                          checked={userContext.usedBuildersPreferredLender}
                          onChange={(e) => setUserContext({...userContext, usedBuildersPreferredLender: true})}
                          className="sr-only"
                        />
                        <span className="font-medium">Yes</span>
                      </label>
                      <label className={`flex items-center justify-center p-4 rounded-lg border-2 cursor-pointer transition-all hover:shadow-md ${
                        !userContext.usedBuildersPreferredLender 
                          ? 'border-green-500 bg-green-50 text-green-700' 
                          : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300'
                      }`}>
                        <input
                          type="radio"
                          name="builderLender"
                          value="no"
                          checked={!userContext.usedBuildersPreferredLender}
                          onChange={(e) => setUserContext({...userContext, usedBuildersPreferredLender: false})}
                          className="sr-only"
                        />
                        <span className="font-medium">No</span>
                      </label>
                    </div>
                    
                    {userContext.usedBuildersPreferredLender && (
                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm font-medium text-slate-700 mb-2">Builder name:</label>
                          <input
                            type="text"
                            value={userContext.builderName || ''}
                            onChange={(e) => setUserContext({...userContext, builderName: e.target.value})}
                            className="w-full px-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors text-slate-900 bg-white"
                            placeholder="e.g., LGI Homes, D.R. Horton, etc."
                          />
                        </div>
                        
                        <div>
                          <label className="block text-sm font-medium text-slate-700 mb-3">
                            Did the builder promise to cover any fees?
                          </label>
                          <div className="space-y-2">
                            {[
                              { key: 'builderPromisedToCoverTitleFees', label: 'Title insurance fees' },
                              { key: 'builderPromisedToCoverEscrowFees', label: 'Escrow/settlement fees' },
                              { key: 'builderPromisedToCoverInspection', label: 'Home inspection fees' }
                            ].map(({ key, label }) => (
                              <label key={key} className={`flex items-center p-3 rounded-lg border cursor-pointer transition-all hover:shadow-sm ${
                                userContext[key as keyof UserContext] 
                                  ? 'border-green-300 bg-green-50' 
                                  : 'border-slate-200 bg-white hover:border-slate-300'
                              }`}>
                                <input
                                  type="checkbox"
                                  checked={userContext[key as keyof UserContext] as boolean}
                                  onChange={(e) => setUserContext({...userContext, [key]: e.target.checked})}
                                  className="w-4 h-4 text-green-600 border-slate-300 rounded focus:ring-green-500 focus:ring-2"
                                />
                                <span className="ml-3 text-slate-800">{label}</span>
                              </label>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Buyer Representation Card */}
                  <div className="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-xl p-6 border border-purple-100">
                    <label className="block text-xl font-semibold text-slate-900 mb-4 flex items-center">
                      <svg className="w-5 h-5 text-purple-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                      Did you have your own buyer's agent?
                    </label>
                    <div className="grid grid-cols-2 gap-3 mb-4">
                      <label className={`flex items-center justify-center p-4 rounded-lg border-2 cursor-pointer transition-all hover:shadow-md ${
                        userContext.hadBuyerAgent 
                          ? 'border-purple-500 bg-purple-50 text-purple-700' 
                          : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300'
                      }`}>
                        <input
                          type="radio"
                          name="buyerAgent"
                          value="yes"
                          checked={userContext.hadBuyerAgent}
                          onChange={(e) => setUserContext({...userContext, hadBuyerAgent: true})}
                          className="sr-only"
                        />
                        <span className="font-medium">Yes</span>
                      </label>
                      <label className={`flex items-center justify-center p-4 rounded-lg border-2 cursor-pointer transition-all hover:shadow-md ${
                        !userContext.hadBuyerAgent 
                          ? 'border-purple-500 bg-purple-50 text-purple-700' 
                          : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300'
                      }`}>
                        <input
                          type="radio"
                          name="buyerAgent"
                          value="no"
                          checked={!userContext.hadBuyerAgent}
                          onChange={(e) => setUserContext({...userContext, hadBuyerAgent: false})}
                          className="sr-only"
                        />
                        <span className="font-medium">No</span>
                      </label>
                    </div>
                    
                    {userContext.hadBuyerAgent && (
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">Agent name:</label>
                        <input
                          type="text"
                          value={userContext.buyerAgentName || ''}
                          onChange={(e) => setUserContext({...userContext, buyerAgentName: e.target.value})}
                          className="w-full px-3 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors text-slate-900 bg-white"
                          placeholder="Your buyer's agent name"
                        />
                      </div>
                    )}
                  </div>
                </div>

                <div className="mt-8">
                  <button
                    onClick={handleContextSubmit}
                    className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-4 px-6 rounded-xl font-semibold hover:from-blue-700 hover:to-blue-800 transition-all transform hover:scale-[1.02] shadow-lg"
                  >
                    Continue to Upload
                  </button>
                </div>
              </div>
            )}

            {/* Upload Section */}
            {currentStep === 'upload' && (
              <div className="animate-in slide-in-from-right duration-300">
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-bold text-slate-900 mb-3">Upload your closing document</h2>
                  <p className="text-lg text-slate-600">We'll analyze it against your expectations to catch any fraud or deception.</p>
                  <button
                    onClick={handleBackToContext}
                    className="inline-flex items-center mt-4 text-blue-600 hover:text-blue-700 text-sm font-medium"
                  >
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                    </svg>
                    Edit your details
                  </button>
                </div>
            
                <div
                  className={`border-2 border-dashed rounded-xl p-12 text-center transition-all duration-300 ${
                    selectedFile 
                      ? 'border-green-300 bg-green-50' 
                      : 'border-slate-300 bg-slate-50 hover:border-blue-400 hover:bg-blue-50'
                  }`}
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                >
                  <div className="mb-6">
                    {selectedFile ? (
                      <svg className="mx-auto h-16 w-16 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    ) : (
                      <svg className="mx-auto h-16 w-16 text-slate-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    )}
                  </div>
                  
                  <div className="mb-6">
                    <label htmlFor="file-upload" className="cursor-pointer">
                      <span className={`text-xl font-semibold ${selectedFile ? 'text-green-700' : 'text-blue-600 hover:text-blue-500'}`}>
                        {selectedFile ? 'File ready!' : 'Click to upload'}
                      </span>
                      {!selectedFile && <span className="text-slate-500"> or drag and drop</span>}
                    </label>
                    <input
                      id="file-upload"
                      type="file"
                      accept=".pdf"
                      onChange={handleFileSelect}
                      className="hidden"
                    />
                  </div>
                  
                  <p className="text-sm text-slate-500">PDF files only • Max 10MB</p>
                </div>

                {selectedFile && (
                  <div className="mt-6 p-4 bg-green-50 rounded-xl border border-green-200">
                    <div className="flex items-center">
                      <svg className="w-5 h-5 text-green-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <div>
                        <p className="font-medium text-green-900">{selectedFile.name}</p>
                        <p className="text-sm text-green-700">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                      </div>
                    </div>
                  </div>
                )}

                {error && (
                  <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl">
                    <div className="flex items-center">
                      <svg className="w-5 h-5 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L5.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                      </svg>
                      <p className="text-red-800">{error}</p>
                    </div>
                  </div>
                )}

                <div className="mt-8">
                  <button
                    onClick={handleUpload}
                    disabled={!selectedFile || uploading}
                    className={`w-full py-4 px-6 rounded-xl font-semibold transition-all transform ${
                      !selectedFile || uploading
                        ? 'bg-slate-300 text-slate-500 cursor-not-allowed'
                        : 'bg-gradient-to-r from-blue-600 to-blue-700 text-white hover:from-blue-700 hover:to-blue-800 hover:scale-[1.02] shadow-lg'
                    }`}
                  >
                    {uploading ? (
                      <div className="flex items-center justify-center">
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Analyzing Document...
                      </div>
                    ) : (
                      'Analyze Document'
                    )}
                  </button>
                </div>
              </div>
            )}

            {/* Results Section */}
            {currentStep === 'results' && report && (
              <div className="animate-in slide-in-from-bottom duration-300">
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-bold text-slate-900 mb-3">Analysis Complete</h2>
                  <button
                    onClick={handleBackToContext}
                    className="inline-flex items-center text-blue-600 hover:text-blue-700 text-sm font-medium"
                  >
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                    </svg>
                    Start over with new document
                  </button>
                </div>

                {/* Forensic Score Dashboard */}
                {report.analytics && (
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                    {/* Forensic Score */}
                    <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-6">
                      <div className="flex items-center">
                        <div className="p-3 rounded-lg bg-gradient-to-br from-purple-500 to-purple-600 mr-4">
                          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                          </svg>
                        </div>
                        <div>
                          <p className="text-sm text-slate-600 font-medium">Forensic Score</p>
                          <p className={`text-2xl font-bold ${
                            report.analytics.forensic_score < 30 
                              ? 'text-red-600' 
                              : report.analytics.forensic_score < 70 
                              ? 'text-yellow-600' 
                              : 'text-green-600'
                          }`}>
                            {report.analytics.forensic_score}/100
                          </p>
                          <p className={`text-xs font-medium ${
                            report.analytics.forensic_score < 30 
                              ? 'text-red-600' 
                              : report.analytics.forensic_score < 70 
                              ? 'text-yellow-600' 
                              : 'text-green-600'
                          }`}>
                            {report.analytics.forensic_score < 30 
                              ? 'HIGH RISK' 
                              : report.analytics.forensic_score < 70 
                              ? 'MODERATE RISK' 
                              : 'LOW RISK'}
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* Total Red Flags */}
                    <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-6">
                      <div className="flex items-center">
                        <div className="p-3 rounded-lg bg-gradient-to-br from-red-500 to-red-600 mr-4">
                          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9" />
                          </svg>
                        </div>
                        <div>
                          <p className="text-sm text-slate-600 font-medium">Red Flags</p>
                          <p className="text-2xl font-bold text-red-600">{report.analytics.total_flags}</p>
                          <p className="text-xs text-slate-500">Issues detected</p>
                        </div>
                      </div>
                    </div>

                    {/* High Severity */}
                    <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-6">
                      <div className="flex items-center">
                        <div className="p-3 rounded-lg bg-gradient-to-br from-orange-500 to-red-500 mr-4">
                          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 18.5c-.77.833.192 2.5 1.732 2.5z" />
                          </svg>
                        </div>
                        <div>
                          <p className="text-sm text-slate-600 font-medium">Critical Issues</p>
                          <p className="text-2xl font-bold text-orange-600">{report.analytics.high_severity}</p>
                          <p className="text-xs text-slate-500">High severity</p>
                        </div>
                      </div>
                    </div>

                    {/* Risk Assessment */}
                    <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-6">
                      <div className="flex items-center">
                        <div className={`p-3 rounded-lg mr-4 ${
                          report.analytics.forensic_score < 30 
                            ? 'bg-gradient-to-br from-red-500 to-red-600' 
                            : report.analytics.forensic_score < 70 
                            ? 'bg-gradient-to-br from-yellow-500 to-orange-500' 
                            : 'bg-gradient-to-br from-green-500 to-green-600'
                        }`}>
                          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                          </svg>
                        </div>
                        <div>
                          <p className="text-sm text-slate-600 font-medium">Protection Level</p>
                          <p className={`text-lg font-bold ${
                            report.analytics.forensic_score < 30 
                              ? 'text-red-600' 
                              : report.analytics.forensic_score < 70 
                              ? 'text-yellow-600' 
                              : 'text-green-600'
                          }`}>
                            {report.analytics.forensic_score < 30 
                              ? '🚨 URGENT' 
                              : report.analytics.forensic_score < 70 
                              ? '⚠️ REVIEW' 
                              : '✅ SECURE'}
                          </p>
                          <p className="text-xs text-slate-500">
                            {report.analytics.forensic_score < 30 
                              ? 'Action needed' 
                              : report.analytics.forensic_score < 70 
                              ? 'Monitor closely' 
                              : 'Well protected'}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                
                <div className="bg-slate-50 rounded-xl p-6 mb-8">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-lg font-medium text-slate-700">Document Status:</span>
                    <span className={`px-4 py-2 rounded-full text-sm font-semibold ${
                      report.flags.length > 0 
                        ? 'bg-red-100 text-red-800' 
                        : 'bg-green-100 text-green-800'
                    }`}>
                      {report.flags.length > 0 ? `⚠️ ${report.flags.length} Issues Found` : '✓ Clean'}
                    </span>
                  </div>
                  
                  {report.metadata && (
                    <div className="text-sm text-slate-600">
                      <p>File: <span className="font-medium">{report.metadata.filename}</span></p>
                      <p>Analyzed: <span className="font-medium">{report.metadata.text_length.toLocaleString()}</span> characters</p>
                    </div>
                  )}
                </div>

                {report.flags.length > 0 ? (
                  <div className="space-y-4">
                    {report.flags.map((flag, index) => (
                      <div key={index} className={`rounded-xl border-2 overflow-hidden transition-all hover:shadow-lg ${getSeverityColor(flag.message)}`}>
                        <div className="p-6">
                          <div className="flex items-start justify-between mb-3">
                            <div className="flex items-center">
                              <span className="text-2xl mr-3">{getSeverityIcon(flag.message)}</span>
                              <h4 className={`text-lg font-bold ${getSeverityTextColor(flag.message)}`}>
                                {flag.rule.replace(/_/g, ' ').toUpperCase()}
                              </h4>
                            </div>
                          </div>
                          <p className={`text-lg mb-4 ${getSeverityTextColor(flag.message)}`}>{flag.message}</p>
                          <details className="group">
                            <summary className="cursor-pointer text-sm font-medium text-slate-600 hover:text-slate-800 transition-colors">
                              View document evidence
                            </summary>
                            <div className="mt-3 p-4 bg-white border border-slate-200 rounded-lg">
                              <p className="text-sm text-slate-700 font-mono leading-relaxed">{flag.snippet}</p>
                            </div>
                          </details>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-16">
                    <div className="text-green-500 text-8xl mb-6">✓</div>
                    <h3 className="text-2xl font-bold text-green-700 mb-3">No Issues Found</h3>
                    <p className="text-lg text-slate-600 max-w-md mx-auto">
                      Your document passed all validation checks. No predatory practices or fraud detected.
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}