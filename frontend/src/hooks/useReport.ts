/**
 * Custom hook for managing report state and API interactions
 */

import { useState, useCallback } from 'react';
import { Report, UserContext } from '@/types';
import { api, ApiError } from '@/services/api';

export const useReport = () => {
  const [report, setReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeDocument = useCallback(async (file: File, context: UserContext): Promise<Report | null> => {
    setLoading(true);
    setError(null);
    setReport(null);

    try {
      // Upload document and get report ID
      const reportId = await api.uploadDocument(file, context);
      
      // Fetch the analysis report
      const reportData = await api.getReport(reportId);
      
      setReport(reportData);
      return reportData;
    } catch (err) {
      const errorMessage = err instanceof ApiError 
        ? err.message 
        : err instanceof Error 
        ? err.message 
        : 'An unexpected error occurred';
      
      setError(errorMessage);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchReport = useCallback(async (reportId: string): Promise<Report | null> => {
    setLoading(true);
    setError(null);

    try {
      const reportData = await api.getReport(reportId);
      setReport(reportData);
      return reportData;
    } catch (err) {
      const errorMessage = err instanceof ApiError 
        ? err.message 
        : err instanceof Error 
        ? err.message 
        : 'Failed to fetch report';
      
      setError(errorMessage);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const clearReport = useCallback(() => {
    setReport(null);
    setError(null);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Computed properties
  const hasReport = report !== null;
  const hasFlags = report && report.flags && report.flags.length > 0;
  const forensicScore = report?.analytics?.forensic_score ?? null;
  const flagCount = report?.flags?.length ?? 0;

  const getRiskLevel = useCallback(() => {
    if (!forensicScore) return null;
    if (forensicScore >= 70) return 'low';
    if (forensicScore >= 30) return 'moderate';
    return 'high';
  }, [forensicScore]);

  const getScoreColor = useCallback(() => {
    const riskLevel = getRiskLevel();
    switch (riskLevel) {
      case 'low': return 'text-green-600 bg-green-50';
      case 'moderate': return 'text-yellow-600 bg-yellow-50';
      case 'high': return 'text-red-600 bg-red-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  }, [getRiskLevel]);

  const getFlagsByCategory = useCallback(() => {
    if (!report?.flags) return { high: [], medium: [], low: [] };

    return report.flags.reduce((acc, flag) => {
      const message = flag.message.toLowerCase();
      if (message.includes('🚨') || message.includes('critical') || message.includes('error') || message.includes('fraud')) {
        acc.high.push(flag);
      } else if (message.includes('⚠️') || message.includes('warning') || message.includes('dangerous') || message.includes('excessive')) {
        acc.medium.push(flag);
      } else {
        acc.low.push(flag);
      }
      return acc;
    }, { high: [] as typeof report.flags, medium: [] as typeof report.flags, low: [] as typeof report.flags });
  }, [report]);

  return {
    report,
    loading,
    error,
    hasReport,
    hasFlags,
    forensicScore,
    flagCount,
    analyzeDocument,
    fetchReport,
    clearReport,
    clearError,
    getRiskLevel,
    getScoreColor,
    getFlagsByCategory,
  };
};