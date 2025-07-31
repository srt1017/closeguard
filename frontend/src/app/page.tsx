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

  return (
    <div className="min-h-screen bg-gray-100 py-12">
      <div className="max-w-4xl mx-auto px-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            CloseGuard
          </h1>
          <p className="text-xl text-gray-600">
            AI-powered analysis for home closing documents
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8">
          {/* Progress Indicator */}
          <div className="mb-8">
            <div className="flex items-center justify-between">
              <div className={`flex items-center ${currentStep === 'context' ? 'text-blue-600' : currentStep === 'upload' || currentStep === 'results' ? 'text-green-600' : 'text-gray-400'}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${currentStep === 'context' ? 'bg-blue-600 text-white' : currentStep === 'upload' || currentStep === 'results' ? 'bg-green-600 text-white' : 'bg-gray-200'}`}>
                  1
                </div>
                <span className="ml-2 text-sm font-medium">Your Situation</span>
              </div>
              <div className={`flex items-center ${currentStep === 'upload' ? 'text-blue-600' : currentStep === 'results' ? 'text-green-600' : 'text-gray-400'}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${currentStep === 'upload' ? 'bg-blue-600 text-white' : currentStep === 'results' ? 'bg-green-600 text-white' : 'bg-gray-200'}`}>
                  2
                </div>
                <span className="ml-2 text-sm font-medium">Upload Document</span>
              </div>
              <div className={`flex items-center ${currentStep === 'results' ? 'text-blue-600' : 'text-gray-400'}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${currentStep === 'results' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>
                  3
                </div>
                <span className="ml-2 text-sm font-medium">Analysis Results</span>
              </div>
            </div>
          </div>

          {/* Context Form */}
          {currentStep === 'context' && (
            <div>
              <h2 className="text-2xl font-semibold mb-6">Tell us about your loan expectations</h2>
              <p className="text-gray-600 mb-8">Help us provide more accurate analysis by answering these questions about what you were promised.</p>
              
              <div className="space-y-8">
                {/* Loan Type */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    What type of loan were you expecting?
                  </label>
                  <div className="space-y-2">
                    {(['FHA', 'Conventional', 'VA', 'USDA', 'Not sure'] as const).map((type) => (
                      <label key={type} className="flex items-center">
                        <input
                          type="radio"
                          name="loanType"
                          value={type}
                          checked={userContext.expectedLoanType === type}
                          onChange={(e) => setUserContext({...userContext, expectedLoanType: e.target.value as any})}
                          className="mr-3 text-blue-600"
                        />
                        <span className="text-gray-700">{type} Loan</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Cost Promises */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Were you promised any of the following?
                  </label>
                  <div className="space-y-3">
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={userContext.promisedZeroClosingCosts}
                        onChange={(e) => setUserContext({...userContext, promisedZeroClosingCosts: e.target.checked})}
                        className="mr-3 text-blue-600"
                      />
                      <span className="text-gray-700">Zero closing costs</span>
                    </label>
                    
                    <div className="ml-6 space-y-2">
                      <div className="flex items-center space-x-2">
                        <label className="text-sm text-gray-600">Lender credit: $</label>
                        <input
                          type="number"
                          value={userContext.promisedLenderCredit || ''}
                          onChange={(e) => setUserContext({...userContext, promisedLenderCredit: e.target.value ? Number(e.target.value) : undefined})}
                          className="w-24 px-2 py-1 border border-gray-300 rounded text-sm"
                          placeholder="0"
                        />
                      </div>
                      <div className="flex items-center space-x-2">
                        <label className="text-sm text-gray-600">Seller credit: $</label>
                        <input
                          type="number"
                          value={userContext.promisedSellerCredit || ''}
                          onChange={(e) => setUserContext({...userContext, promisedSellerCredit: e.target.value ? Number(e.target.value) : undefined})}
                          className="w-24 px-2 py-1 border border-gray-300 rounded text-sm"
                          placeholder="0"
                        />
                      </div>
                      <div className="flex items-center space-x-2">
                        <label className="text-sm text-gray-600">Builder rebate: $</label>
                        <input
                          type="number"
                          value={userContext.promisedRebate || ''}
                          onChange={(e) => setUserContext({...userContext, promisedRebate: e.target.value ? Number(e.target.value) : undefined})}
                          className="w-24 px-2 py-1 border border-gray-300 rounded text-sm"
                          placeholder="0"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Builder Relationship */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Did you use the builder's preferred/recommended lender?
                  </label>
                  <div className="space-y-2">
                    <label className="flex items-center">
                      <input
                        type="radio"
                        name="builderLender"
                        value="yes"
                        checked={userContext.usedBuildersPreferredLender}
                        onChange={(e) => setUserContext({...userContext, usedBuildersPreferredLender: true})}
                        className="mr-3 text-blue-600"
                      />
                      <span className="text-gray-700">Yes</span>
                    </label>
                    <label className="flex items-center">
                      <input
                        type="radio"
                        name="builderLender"
                        value="no"
                        checked={!userContext.usedBuildersPreferredLender}
                        onChange={(e) => setUserContext({...userContext, usedBuildersPreferredLender: false})}
                        className="mr-3 text-blue-600"
                      />
                      <span className="text-gray-700">No</span>
                    </label>
                  </div>
                  
                  {userContext.usedBuildersPreferredLender && (
                    <div className="mt-3">
                      <label className="block text-sm text-gray-600 mb-1">Builder name:</label>
                      <input
                        type="text"
                        value={userContext.builderName || ''}
                        onChange={(e) => setUserContext({...userContext, builderName: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded"
                        placeholder="e.g., LGI Homes, D.R. Horton, etc."
                      />
                    </div>
                  )}
                </div>

                {/* Builder Promises */}
                {userContext.usedBuildersPreferredLender && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-3">
                      Did the builder promise to cover any of these fees?
                    </label>
                    <div className="space-y-2">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={userContext.builderPromisedToCoverTitleFees}
                          onChange={(e) => setUserContext({...userContext, builderPromisedToCoverTitleFees: e.target.checked})}
                          className="mr-3 text-blue-600"
                        />
                        <span className="text-gray-700">Title insurance fees</span>
                      </label>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={userContext.builderPromisedToCoverEscrowFees}
                          onChange={(e) => setUserContext({...userContext, builderPromisedToCoverEscrowFees: e.target.checked})}
                          className="mr-3 text-blue-600"
                        />
                        <span className="text-gray-700">Escrow/settlement fees</span>
                      </label>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={userContext.builderPromisedToCoverInspection}
                          onChange={(e) => setUserContext({...userContext, builderPromisedToCoverInspection: e.target.checked})}
                          className="mr-3 text-blue-600"
                        />
                        <span className="text-gray-700">Home inspection fees</span>
                      </label>
                    </div>
                  </div>
                )}

                {/* Buyer Representation */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Did you have your own buyer's agent/realtor?
                  </label>
                  <div className="space-y-2">
                    <label className="flex items-center">
                      <input
                        type="radio"
                        name="buyerAgent"
                        value="yes"
                        checked={userContext.hadBuyerAgent}
                        onChange={(e) => setUserContext({...userContext, hadBuyerAgent: true})}
                        className="mr-3 text-blue-600"
                      />
                      <span className="text-gray-700">Yes</span>
                    </label>
                    <label className="flex items-center">
                      <input
                        type="radio"
                        name="buyerAgent"
                        value="no"
                        checked={!userContext.hadBuyerAgent}
                        onChange={(e) => setUserContext({...userContext, hadBuyerAgent: false})}
                        className="mr-3 text-blue-600"
                      />
                      <span className="text-gray-700">No</span>
                    </label>
                  </div>
                  
                  {userContext.hadBuyerAgent && (
                    <div className="mt-3">
                      <label className="block text-sm text-gray-600 mb-1">Agent name:</label>
                      <input
                        type="text"
                        value={userContext.buyerAgentName || ''}
                        onChange={(e) => setUserContext({...userContext, buyerAgentName: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded"
                        placeholder="Your buyer's agent name"
                      />
                    </div>
                  )}
                </div>
              </div>

              <div className="mt-8">
                <button
                  onClick={handleContextSubmit}
                  className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
                >
                  Continue to Upload
                </button>
              </div>
            </div>
          )}

          {/* Upload Section */}
          {currentStep === 'upload' && (
            <div className="mb-8">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-semibold">Upload PDF Document</h2>
                <button
                  onClick={handleBackToContext}
                  className="text-blue-600 hover:text-blue-700 text-sm font-medium"
                >
                  ← Edit your situation
                </button>
              </div>
            
            <div
              className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors"
              onDragOver={handleDragOver}
              onDrop={handleDrop}
            >
              <div className="mb-4">
                <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>
              
              <div className="mb-4">
                <label htmlFor="file-upload" className="cursor-pointer">
                  <span className="text-lg font-medium text-blue-600 hover:text-blue-500">
                    Click to upload
                  </span>
                  <span className="text-gray-500"> or drag and drop</span>
                </label>
                <input
                  id="file-upload"
                  type="file"
                  accept=".pdf"
                  onChange={handleFileSelect}
                  className="hidden"
                />
              </div>
              
              <p className="text-sm text-gray-500">PDF files only</p>
            </div>

            {selectedFile && (
              <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-700">
                  Selected: <span className="font-medium">{selectedFile.name}</span>
                </p>
              </div>
            )}

            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-700">{error}</p>
              </div>
            )}

            <div className="mt-6">
              <button
                onClick={handleUpload}
                disabled={!selectedFile || uploading}
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {uploading ? 'Analyzing...' : 'Analyze Document'}
              </button>
            </div>
          </div>

          )}

          {/* Results Section */}
          {currentStep === 'results' && report && (
            <div className="border-t pt-8">
              <h2 className="text-2xl font-semibold mb-6">Analysis Results</h2>
              
              <div className="mb-6">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-lg font-medium">Status:</span>
                  <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                    {report.status}
                  </span>
                </div>
                
                {report.metadata && (
                  <div className="text-sm text-gray-600 mb-4">
                    <p>File: {report.metadata.filename}</p>
                    <p>Text extracted: {report.metadata.text_length.toLocaleString()} characters</p>
                  </div>
                )}
              </div>

              {report.flags.length > 0 ? (
                <div>
                  <h3 className="text-lg font-semibold mb-4 text-red-700">
                    ⚠️ Issues Found ({report.flags.length})
                  </h3>
                  <div className="space-y-4">
                    {report.flags.map((flag, index) => (
                      <div key={index} className="border border-red-200 rounded-lg p-4 bg-red-50">
                        <div className="flex items-start justify-between mb-2">
                          <h4 className="font-medium text-red-900">{flag.rule.replace(/_/g, ' ').toUpperCase()}</h4>
                        </div>
                        <p className="text-red-800 mb-2">{flag.message}</p>
                        <div className="bg-white border rounded p-2">
                          <p className="text-sm text-gray-700 font-mono">{flag.snippet}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="text-center py-8">
                  <div className="text-green-600 text-6xl mb-4">✓</div>
                  <h3 className="text-lg font-semibold text-green-700 mb-2">No Issues Found</h3>
                  <p className="text-gray-600">Your document passed all validation checks.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
