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

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [report, setReport] = useState<Report | null>(null);
  const [error, setError] = useState<string | null>(null);

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
      // Upload PDF
      const formData = new FormData();
      formData.append('file', selectedFile);

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
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setUploading(false);
    }
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
          {/* Upload Section */}
          <div className="mb-8">
            <h2 className="text-2xl font-semibold mb-6">Upload PDF Document</h2>
            
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

          {/* Results Section */}
          {report && (
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
