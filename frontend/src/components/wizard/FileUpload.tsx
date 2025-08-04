/**
 * File upload component with drag-and-drop support
 */

import React from 'react';
import { Button } from '@/components/ui';

interface FileUploadProps {
  selectedFile: File | null;
  uploading: boolean;
  error: string | null;
  onFileSelect: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onFileDrop: (event: React.DragEvent<HTMLDivElement>) => void;
  onDragOver: (event: React.DragEvent<HTMLDivElement>) => void;
  onUpload: () => void;
  onBackToContext: () => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  selectedFile,
  uploading,
  error,
  onFileSelect,
  onFileDrop,
  onDragOver,
  onUpload,
  onBackToContext
}) => {
  return (
    <div className="animate-in slide-in-from-right duration-300">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-slate-900 mb-3">Upload your closing document</h2>
        <p className="text-lg text-slate-600">We'll analyze it against your expectations to catch any fraud or deception.</p>
        <button
          onClick={onBackToContext}
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
        onDragOver={onDragOver}
        onDrop={onFileDrop}
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
            onChange={onFileSelect}
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

      <div className="flex gap-4 mt-8">
        <Button
          onClick={onBackToContext}
          variant="secondary"
          className="flex-1"
        >
          Back
        </Button>
        <Button
          onClick={onUpload}
          variant="primary"
          className="flex-1"
          disabled={!selectedFile || uploading}
          loading={uploading}
        >
          {uploading ? 'Analyzing...' : 'Analyze Document'}
        </Button>
      </div>
    </div>
  );
};