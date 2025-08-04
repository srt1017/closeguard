/**
 * Custom hook for managing file upload state and logic
 */

import { useState, useCallback } from 'react';

export const useFileUpload = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError(null);
    } else {
      setError('Please select a PDF file');
      setSelectedFile(null);
    }
  }, []);

  const handleFileDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
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
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  }, []);

  const clearFile = useCallback(() => {
    setSelectedFile(null);
    setError(null);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // File validation
  const isFileValid = useCallback((file: File | null): boolean => {
    if (!file) return false;
    if (file.type !== 'application/pdf') return false;
    if (file.size > 50 * 1024 * 1024) return false; // 50MB limit
    return true;
  }, []);

  const getFileInfo = useCallback(() => {
    if (!selectedFile) return null;
    
    return {
      name: selectedFile.name,
      size: selectedFile.size,
      sizeFormatted: `${(selectedFile.size / (1024 * 1024)).toFixed(1)} MB`,
      type: selectedFile.type,
      lastModified: new Date(selectedFile.lastModified),
    };
  }, [selectedFile]);

  return {
    selectedFile,
    uploading,
    error,
    handleFileSelect,
    handleFileDrop,
    handleDragOver,
    clearFile,
    clearError,
    setUploading,
    setError,
    isFileValid,
    getFileInfo,
  };
};